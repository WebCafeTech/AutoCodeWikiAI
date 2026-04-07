#!/usr/bin/env python3
"""
FastAPI chat endpoints for interactive Q&A over generated documentation.

Endpoint:
    POST /api/chat/{job_id}
        Request body: {"message": "...", "session_id": "..."}
        Response: text/event-stream (Server-Sent Events)

Chat history is kept **in-memory** per (job_id, session_id) pair.  It
persists for the lifetime of the server process, which satisfies the
requirement that "chat history persists for the session".
"""

import re
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .chat_service import stream_chat_response

router = APIRouter()

# In-memory chat history: {(job_id, session_id): [{"role": ..., "content": ...}]}
_chat_histories: Dict[tuple, List[Dict[str, str]]] = {}

# Docs root – resolved once from the environment / config so all requests use
# the same base directory.  Can be overridden for testing.
_DOCS_ROOT = Path("output") / "docs"

# Job IDs are derived from GitHub repo full-names like "owner--repo".
# Only allow alphanumeric chars, hyphens, underscores, and dots.
_JOB_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class ChatRequest(BaseModel):
    """Request body for POST /api/chat/{job_id}."""
    message: str
    session_id: str = "default"


def _validate_job_id(job_id: str) -> None:
    """Raise 400 if *job_id* contains path-traversal or unexpected characters."""
    if not _JOB_ID_RE.match(job_id) or ".." in job_id:
        raise HTTPException(status_code=400, detail="Invalid job ID")


def _get_history(job_id: str, session_id: str) -> List[Dict[str, str]]:
    key = (job_id, session_id)
    if key not in _chat_histories:
        _chat_histories[key] = []
    return _chat_histories[key]


def _append_history(
    job_id: str,
    session_id: str,
    role: str,
    content: str,
) -> None:
    _get_history(job_id, session_id).append({"role": role, "content": content})


@router.post("/api/chat/{job_id}")
async def chat(job_id: str, body: ChatRequest):
    """
    Stream an LLM response to *body.message* using RAG over the docs for
    *job_id*.

    The response is a ``text/event-stream`` stream.  Each event carries one or
    more tokens of the assistant's reply.  A final ``data: [DONE]`` event
    signals the end of the stream.
    """
    _validate_job_id(job_id)

    # Resolve and canonicalise the docs path; reject any traversal attempts.
    docs_path = (_DOCS_ROOT / f"{job_id}-docs").resolve()
    expected_root = _DOCS_ROOT.resolve()
    if not str(docs_path).startswith(str(expected_root)):
        raise HTTPException(status_code=400, detail="Invalid job ID")
    if not docs_path.exists():
        raise HTTPException(status_code=404, detail="Documentation not found for this job")

    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message must not be empty")

    # Retrieve or create history for this session
    history = _get_history(job_id, body.session_id)

    # Collect assistant reply so we can persist it to history afterwards
    assistant_reply_parts: List[str] = []

    async def _event_generator():
        async for token in stream_chat_response(job_id, docs_path, message, history):
            if token == "[DONE]":
                # Persist turn to history now that streaming has finished
                full_reply = "".join(assistant_reply_parts)
                _append_history(job_id, body.session_id, "user", message)
                _append_history(job_id, body.session_id, "assistant", full_reply)
                yield "data: [DONE]\n\n"
            else:
                assistant_reply_parts.append(token)
                # Escape newlines inside the data field per SSE spec
                safe_token = token.replace("\n", "\\n")
                yield f"data: {safe_token}\n\n"

    return StreamingResponse(_event_generator(), media_type="text/event-stream")


@router.delete("/api/chat/{job_id}/history")
async def clear_history(job_id: str, session_id: str = "default"):
    """Clear chat history for *job_id* / *session_id*."""
    _validate_job_id(job_id)
    key = (job_id, session_id)
    _chat_histories.pop(key, None)
    return {"status": "cleared"}
