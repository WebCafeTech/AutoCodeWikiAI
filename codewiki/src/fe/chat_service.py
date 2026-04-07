#!/usr/bin/env python3
"""
RAG-based chat service for interactive Q&A over generated documentation.

Pipeline:
1. Load all .md files from the job's docs directory
2. Split content into paragraphs (chunks)
3. Retrieve the most relevant chunks via keyword-overlap scoring (BM25-inspired)
4. Build a context-aware prompt and stream the LLM response via SSE
"""

import re
import os
import math
from pathlib import Path
from typing import AsyncGenerator, List, Tuple, Dict


# ---------------------------------------------------------------------------
# Document loading & chunking
# ---------------------------------------------------------------------------

def _load_docs(docs_path: Path) -> List[Tuple[str, str]]:
    """
    Load all markdown files from *docs_path*.

    Returns a list of ``(filename, chunk_text)`` pairs where each chunk is a
    non-empty paragraph from the file.
    """
    chunks: List[Tuple[str, str]] = []
    for md_file in sorted(docs_path.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for para in _split_into_chunks(content):
            chunks.append((md_file.name, para))
    return chunks


def _split_into_chunks(text: str, max_chars: int = 1500) -> List[str]:
    """
    Split *text* into chunks of at most *max_chars* characters.

    First splits on blank lines (paragraph boundaries), then further splits
    any paragraph that exceeds *max_chars* by sentence boundaries.
    """
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: List[str] = []
    for para in paragraphs:
        if len(para) <= max_chars:
            chunks.append(para)
        else:
            # Split long paragraphs by sentence
            sentences = re.split(r"(?<=[.!?])\s+", para)
            current = ""
            for sentence in sentences:
                if len(current) + len(sentence) + 1 <= max_chars:
                    current = (current + " " + sentence).strip()
                else:
                    if current:
                        chunks.append(current)
                    current = sentence
            if current:
                chunks.append(current)
    return chunks


# ---------------------------------------------------------------------------
# Retrieval (keyword BM25-inspired scoring, no external dependencies)
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> List[str]:
    """Lowercase word-tokenise *text*, removing punctuation."""
    return re.findall(r"\b[a-z0-9_]+\b", text.lower())


def _build_idf(chunks: List[Tuple[str, str]]) -> Dict[str, float]:
    """Compute inverse document frequency for each token across all chunks."""
    n = len(chunks)
    if n == 0:
        return {}
    df: Dict[str, int] = {}
    for _, text in chunks:
        for token in set(_tokenize(text)):
            df[token] = df.get(token, 0) + 1
    return {token: math.log((n - freq + 0.5) / (freq + 0.5) + 1.0) for token, freq in df.items()}


def _bm25_score(
    query_tokens: List[str],
    doc_tokens: List[str],
    idf: Dict[str, float],
    k1: float = 1.5,
    b: float = 0.75,
    avg_dl: float = 100.0,
) -> float:
    """Compute BM25 score for a single document."""
    dl = len(doc_tokens)
    tf: Dict[str, int] = {}
    for t in doc_tokens:
        tf[t] = tf.get(t, 0) + 1

    score = 0.0
    for token in query_tokens:
        if token not in idf:
            continue
        f = tf.get(token, 0)
        numerator = f * (k1 + 1)
        denominator = f + k1 * (1 - b + b * dl / max(avg_dl, 1))
        score += idf[token] * numerator / max(denominator, 1e-9)
    return score


def retrieve_relevant_chunks(
    query: str,
    chunks: List[Tuple[str, str]],
    top_k: int = 5,
) -> List[Tuple[str, str]]:
    """
    Return the *top_k* most relevant ``(filename, chunk_text)`` pairs for *query*.

    Uses a lightweight BM25-inspired scoring function so no external libraries
    are required.
    """
    if not chunks:
        return []

    idf = _build_idf(chunks)
    query_tokens = _tokenize(query)
    avg_dl = sum(len(_tokenize(text)) for _, text in chunks) / len(chunks)

    scored: List[Tuple[float, int]] = []
    for i, (_, text) in enumerate(chunks):
        doc_tokens = _tokenize(text)
        score = _bm25_score(query_tokens, doc_tokens, idf, avg_dl=avg_dl)
        scored.append((score, i))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunks[i] for _, i in scored[:top_k]]


# ---------------------------------------------------------------------------
# LLM streaming
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a helpful documentation assistant.  You answer questions about a \
software repository based solely on the provided documentation excerpts.

Rules:
- Only use information from the provided excerpts.
- When citing information, mention the source file in parentheses, \
  e.g. (overview.md).
- If the answer is not found in the excerpts, say so clearly.
- Format code examples with markdown code blocks.
"""


def _build_context(relevant_chunks: List[Tuple[str, str]]) -> str:
    """Format retrieved chunks as a context block for the LLM prompt."""
    if not relevant_chunks:
        return "(No relevant documentation excerpts found.)"
    parts: List[str] = []
    for filename, text in relevant_chunks:
        parts.append(f"--- {filename} ---\n{text}")
    return "\n\n".join(parts)


async def stream_chat_response(
    job_id: str,
    docs_path: Path,
    message: str,
    history: List[Dict[str, str]],
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields LLM response tokens as Server-Sent Event data.

    Args:
        job_id:     Documentation job identifier (unused in the call itself but
                    useful for logging / future caching).
        docs_path:  Path to the directory containing the generated .md files.
        message:    User's natural-language question.
        history:    List of previous ``{"role": ..., "content": ...}`` messages
                    in the current session.

    Yields:
        Strings of the form ``data: <token>\n\n`` for each streamed token,
        followed by a final ``data: [DONE]\n\n`` sentinel.
    """
    from openai import AsyncOpenAI, APIError

    # Load and retrieve relevant chunks
    chunks = _load_docs(docs_path)
    relevant = retrieve_relevant_chunks(message, chunks, top_k=6)
    context = _build_context(relevant)

    # Build messages list
    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Include up to the last 10 turns of history to stay within token budget
    messages.extend(history[-10:])
    messages.append(
        {
            "role": "user",
            "content": (
                f"Documentation excerpts:\n\n{context}\n\n"
                f"Question: {message}"
            ),
        }
    )

    # Read LLM config from environment (same variables used by the web app and
    # the CLI; falls back to the values defined in codewiki.src.config).
    llm_base_url = os.getenv("LLM_BASE_URL", "http://localhost:4000/")
    llm_api_key = os.getenv("LLM_API_KEY", "sk-1234")
    main_model = os.getenv("MAIN_MODEL", "claude-sonnet-4")

    client = AsyncOpenAI(base_url=llm_base_url, api_key=llm_api_key)

    try:
        stream = await client.chat.completions.create(
            model=main_model,
            messages=messages,  # type: ignore[arg-type]
            stream=True,
            temperature=0.3,
            max_tokens=2048,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield delta.content
    except APIError:
        # Avoid leaking internal error details (e.g. API keys in URLs) to the client.
        yield "\n\n⚠️ The LLM service returned an error. Please try again later."
    finally:
        yield "[DONE]"
