#!/usr/bin/env python3
"""
HTML templates for the CodeWiki web application.
"""

# Web interface HTML template
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeWiki - GitHub Repository Documentation Generator</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #f1f5f9;
            --text-color: #334155;
            --border-color: #e2e8f0;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: var(--primary-color);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .content {
            padding: 2rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .form-group input {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.2s ease;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: var(--primary-color);
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 2rem;
            background: var(--primary-color);
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .btn:hover {
            background: #1d4ed8;
            transform: translateY(-1px);
        }
        
        .btn:disabled {
            background: #94a3b8;
            cursor: not-allowed;
            transform: none;
        }
        
        .alert {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .alert-success {
            background: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }
        
        .alert-error {
            background: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }
        
        .recent-jobs {
            margin-top: 2rem;
            border-top: 1px solid var(--border-color);
            padding-top: 2rem;
        }
        
        .job-item {
            background: var(--secondary-color);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .job-url {
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .job-status {
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 600;
        }
        
        .status-queued {
            background: #fef3c7;
            color: #92400e;
        }
        
        .status-processing {
            background: #dbeafe;
            color: #1e40af;
        }
        
        .status-completed {
            background: #dcfce7;
            color: #166534;
        }
        
        .status-failed {
            background: #fef2f2;
            color: #991b1b;
        }
        
        .job-progress {
            font-size: 0.875rem;
            color: #64748b;
            margin-top: 0.25rem;
        }
        
        .job-actions {
            margin-top: 0.5rem;
        }
        
        .btn-small {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 CodeWiki</h1>
            <p>Generate comprehensive documentation for any GitHub repository</p>
        </div>
        
        <div class="content">
            {% if message %}
            <div class="alert alert-{{ message_type }}">
                {{ message }}
            </div>
            {% endif %}
            
            <form method="POST" action="/">
                <div class="form-group">
                    <label for="repo_url">GitHub Repository URL:</label>
                    <input 
                        type="url" 
                        id="repo_url" 
                        name="repo_url" 
                        placeholder="https://github.com/owner/repository"
                        required
                        value="{{ repo_url or '' }}"
                    >
                </div>
                
                <div class="form-group">
                    <label for="commit_id">Commit ID (optional):</label>
                    <input 
                        type="text" 
                        id="commit_id" 
                        name="commit_id" 
                        placeholder="Enter specific commit hash (defaults to latest)"
                        value="{{ commit_id or '' }}"
                        pattern="[a-f0-9]{4,40}"
                        title="Enter a valid commit hash (4-40 characters, hexadecimal)"
                    >
                </div>
                
                <button type="submit" class="btn">Generate Documentation</button>
            </form>
            
            {% if recent_jobs %}
            <div class="recent-jobs">
                <h3>Recent Jobs</h3>
                {% for job in recent_jobs %}
                <div class="job-item">
                    <div class="job-header">
                        <div class="job-url">{{ job.repo_url }}</div>
                        <div class="job-status status-{{ job.status }}">{{ job.status }}</div>
                    </div>
                    <div class="job-progress">{{ job.progress }}</div>
                    {% if job.main_model %}
                    <div class="job-model" style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">
                        Generated with: {{ job.main_model }}
                    </div>
                    {% endif %}
                    <div class="job-actions">
                        <a href="/docs/{{ job.job_id }}" class="btn btn-small">View Documentation</a>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </div>
    
    <script>
        // Form submission protection
        let isSubmitting = false;
        
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.querySelector('form');
            const submitButton = document.querySelector('button[type="submit"]');
            
            if (form && submitButton) {
                form.addEventListener('submit', function(e) {
                    if (isSubmitting) {
                        e.preventDefault();
                        return false;
                    }
                    
                    isSubmitting = true;
                    submitButton.disabled = true;
                    submitButton.textContent = 'Processing...';
                    
                    // Re-enable after 10 seconds as a failsafe
                    setTimeout(function() {
                        isSubmitting = false;
                        submitButton.disabled = false;
                        submitButton.textContent = 'Generate Documentation';
                    }, 10000);
                });
            }
            
            // Optional: Add manual refresh button instead of auto-refresh
            const refreshButton = document.createElement('button');
            refreshButton.textContent = 'Refresh Status';
            refreshButton.className = 'btn btn-small';
            refreshButton.style.marginTop = '1rem';
            refreshButton.onclick = function() {
                window.location.reload();
            };
            
            const recentJobsSection = document.querySelector('.recent-jobs');
            if (recentJobsSection) {
                recentJobsSection.appendChild(refreshButton);
            }
        });
    </script>
</body>
</html>
"""

# HTML template for the documentation pages
DOCS_VIEW_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.9.0/dist/mermaid.min.js"></script>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #f1f5f9;
            --text-color: #334155;
            --border-color: #e2e8f0;
            --hover-color: #f8fafc;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #ffffff;
        }
        
        .container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 300px;
            background-color: var(--secondary-color);
            border-right: 1px solid var(--border-color);
            padding: 20px;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
        }
        
        .content {
            flex: 1;
            margin-left: 300px;
            padding: 40px 60px;
            max-width: calc(100% - 300px);
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 30px;
            text-decoration: none;
        }
        
        .nav-section {
            margin-bottom: 25px;
        }
        
        .nav-section h3 {
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
        }
        
        .nav-item {
            display: block;
            padding: 8px 12px;
            color: var(--text-color);
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.2s ease;
            margin-bottom: 2px;
        }
        
        .nav-item:hover {
            background-color: var(--hover-color);
            color: var(--primary-color);
        }
        
        .nav-item.active {
            background-color: var(--primary-color);
            color: white;
        }
        
        .nav-subsection {
            margin-left: 15px;
            margin-top: 8px;
        }
        
        .nav-subsection .nav-item {
            font-size: 13px;
            color: #64748b;
        }
        
        .nav-section-header {
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
            padding: 8px 12px;
        }
        
        /* Nested subsection indentation - scalable for any depth */
        .nav-subsection .nav-subsection {
            margin-left: 20px;
        }
        
        .nav-subsection .nav-subsection .nav-item {
            font-size: 12px;
        }
        
        /* Additional nesting levels */
        .nav-subsection .nav-subsection .nav-subsection {
            margin-left: 15px;
        }
        
        .nav-subsection .nav-subsection .nav-subsection .nav-item {
            font-size: 11px;
        }
        
        .markdown-content {
            max-width: none;
        }
        
        .markdown-content h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }
        
        .markdown-content h2 {
            font-size: 2rem;
            font-weight: 600;
            color: #334155;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        .markdown-content h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: #475569;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }
        
        .markdown-content p {
            margin-bottom: 1rem;
            color: #475569;
        }
        
        .markdown-content ul, .markdown-content ol {
            margin-bottom: 1rem;
            padding-left: 1.5rem;
        }
        
        .markdown-content li {
            margin-bottom: 0.5rem;
            color: #475569;
        }
        
        .markdown-content code {
            background-color: #f1f5f9;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 0.875rem;
        }
        
        .markdown-content pre {
            background-color: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            overflow-x: auto;
            margin-bottom: 1rem;
        }
        
        .markdown-content pre code {
            background-color: transparent;
            padding: 0;
        }
        
        .markdown-content blockquote {
            border-left: 4px solid var(--primary-color);
            padding-left: 1rem;
            margin-bottom: 1rem;
            font-style: italic;
            color: #64748b;
        }
        
        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
        }
        
        .markdown-content th, .markdown-content td {
            border: 1px solid var(--border-color);
            padding: 0.75rem;
            text-align: left;
        }
        
        .markdown-content th {
            background-color: var(--secondary-color);
            font-weight: 600;
        }
        
        .markdown-content a {
            color: var(--primary-color);
            text-decoration: underline;
        }
        
        .markdown-content a:hover {
            text-decoration: none;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                position: relative;
                height: auto;
            }
            
            .content {
                margin-left: 0;
                padding: 20px;
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <a href="/static-docs/{{ job_id }}/overview.md" class="logo">📚 {{ repo_name }}</a>
            
            {% if metadata and metadata.generation_info %}
            <div style="margin: 20px 0; padding: 15px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                <h4 style="margin: 0 0 10px 0; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Generation Info</h4>
                <div style="font-size: 11px; color: #475569; line-height: 1.4;">
                    <div style="margin-bottom: 4px;"><strong>Model:</strong> {{ metadata.generation_info.main_model }}</div>
                    <div style="margin-bottom: 4px;"><strong>Generated:</strong> {{ metadata.generation_info.timestamp[:16] }}</div>
                    {% if metadata.generation_info.commit_id %}
                    <div style="margin-bottom: 4px;"><strong>Commit:</strong> {{ metadata.generation_info.commit_id[:8] }}</div>
                    {% endif %}
                    {% if metadata.statistics %}
                    <div><strong>Components:</strong> {{ metadata.statistics.total_components }}</div>
                    {% endif %}
                </div>
            </div>
            {% endif %}
            
            {% if navigation %}
            <div class="nav-section">
                <a href="/static-docs/{{ job_id }}/overview.md" class="nav-item {% if current_page == 'overview.md' %}active{% endif %}">
                    Overview
                </a>
            </div>
            
            {% macro render_nav_item(key, data, depth=0) %}
                {% set indent_class = 'nav-subsection' if depth > 0 else '' %}
                {% set indent_style = 'margin-left: ' + (depth * 15)|string + 'px;' if depth > 0 else '' %}
                <div class="{{ indent_class }}" {% if indent_style %}style="{{ indent_style }}"{% endif %}>
                    {% if data.components %}
                        <a href="/static-docs/{{ job_id }}/{{ key }}.md" class="nav-item {% if current_page == key + '.md' %}active{% endif %}">
                            {{ key.replace('_', ' ').title() }}
                        </a>
                    {% else %}
                        <div class="nav-section-header" {% if depth > 0 %}style="font-size: {{ 14 - (depth * 1) }}px; text-transform: none;"{% endif %}>
                            {{ key.replace('_', ' ').title() }}
                        </div>
                    {% endif %}
                    
                    {% if data.children %}
                        {% for child_key, child_data in data.children.items() %}
                            {{ render_nav_item(child_key, child_data, depth + 1) }}
                        {% endfor %}
                    {% endif %}
                </div>
            {% endmacro %}
            
            {% for section_key, section_data in navigation.items() %}
            <div class="nav-section">
                {{ render_nav_item(section_key, section_data) }}
            </div>
            {% endfor %}
            {% endif %}
        </nav>
        
        <main class="content">
            <div class="markdown-content">
                {{ content | safe }}
            </div>
        </main>
    </div>
    
    <script>
        // Initialize mermaid with configuration
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#2563eb',
                primaryTextColor: '#334155',
                primaryBorderColor: '#e2e8f0',
                lineColor: '#64748b',
                sectionBkgColor: '#f8fafc',
                altSectionBkgColor: '#f1f5f9',
                gridColor: '#e2e8f0',
                secondaryColor: '#f1f5f9',
                tertiaryColor: '#f8fafc'
            },
            flowchart: {
                htmlLabels: true,
                curve: 'basis'
            },
            sequence: {
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35,
                mirrorActors: true,
                bottomMarginAdj: 1,
                useMaxWidth: true,
                rightAngles: false,
                showSequenceNumbers: false
            }
        });
        
        // Re-render mermaid diagrams after page load
        document.addEventListener('DOMContentLoaded', function() {
            mermaid.init(undefined, document.querySelectorAll('.mermaid'));
        });
    </script>

    <!-- ===================== Chat Widget ===================== -->
    <style>
        /* Chat widget – fixed to the bottom-right corner */
        #chat-widget {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 1000;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        #chat-toggle-btn {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--primary-color, #2563eb);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s, transform 0.1s;
        }

        #chat-toggle-btn:hover {
            background: #1d4ed8;
            transform: scale(1.05);
        }

        #chat-panel {
            display: none;
            flex-direction: column;
            width: 380px;
            height: 520px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            border: 1px solid #e2e8f0;
            overflow: hidden;
            margin-bottom: 12px;
        }

        #chat-panel.open {
            display: flex;
        }

        #chat-header {
            background: var(--primary-color, #2563eb);
            color: white;
            padding: 14px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }

        #chat-header span {
            font-weight: 600;
            font-size: 15px;
        }

        #chat-clear-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 12px;
            cursor: pointer;
        }

        #chat-clear-btn:hover {
            background: rgba(255,255,255,0.35);
        }

        #chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .chat-bubble {
            max-width: 88%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .chat-bubble.user {
            background: var(--primary-color, #2563eb);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .chat-bubble.assistant {
            background: #f1f5f9;
            color: #334155;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .chat-bubble.assistant pre {
            background: #e2e8f0;
            padding: 8px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 12px;
            margin: 6px 0;
        }

        .chat-bubble.assistant code {
            background: #e2e8f0;
            padding: 1px 4px;
            border-radius: 3px;
            font-size: 12px;
        }

        .chat-bubble.assistant pre code {
            background: transparent;
            padding: 0;
        }

        #chat-footer {
            padding: 12px;
            border-top: 1px solid #e2e8f0;
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }

        #chat-input {
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            resize: none;
            outline: none;
            line-height: 1.4;
            font-family: inherit;
        }

        #chat-input:focus {
            border-color: var(--primary-color, #2563eb);
        }

        #chat-send-btn {
            background: var(--primary-color, #2563eb);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 14px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.2s;
            align-self: flex-end;
        }

        #chat-send-btn:hover:not(:disabled) {
            background: #1d4ed8;
        }

        #chat-send-btn:disabled {
            background: #94a3b8;
            cursor: not-allowed;
        }

        .chat-typing {
            display: inline-block;
            color: #64748b;
            font-style: italic;
            font-size: 13px;
        }
    </style>

    <div id="chat-widget">
        <div id="chat-panel" role="dialog" aria-label="Documentation chatbot">
            <div id="chat-header">
                <span>💬 Ask about the docs</span>
                <button id="chat-clear-btn" title="Clear chat history">Clear</button>
            </div>
            <div id="chat-messages" aria-live="polite"></div>
            <div id="chat-footer">
                <textarea
                    id="chat-input"
                    rows="1"
                    placeholder="Ask a question about this repository…"
                    aria-label="Chat message input"
                ></textarea>
                <button id="chat-send-btn" title="Send message" aria-label="Send message">➤</button>
            </div>
        </div>
        <button id="chat-toggle-btn" title="Toggle chat" aria-label="Open documentation chatbot">💬</button>
    </div>

    <script>
    (function () {
        var JOB_ID = {{ job_id | tojson }};
        var SESSION_ID = 'session-' + Math.random().toString(36).slice(2);

        var panel    = document.getElementById('chat-panel');
        var toggleBtn = document.getElementById('chat-toggle-btn');
        var clearBtn  = document.getElementById('chat-clear-btn');
        var messages  = document.getElementById('chat-messages');
        var input     = document.getElementById('chat-input');
        var sendBtn   = document.getElementById('chat-send-btn');

        var isOpen = false;
        var isStreaming = false;

        // Toggle panel open/closed
        toggleBtn.addEventListener('click', function () {
            isOpen = !isOpen;
            panel.classList.toggle('open', isOpen);
            toggleBtn.textContent = isOpen ? '✕' : '💬';
            if (isOpen && messages.children.length === 0) {
                appendBubble('assistant', 'Hi! I can answer questions about this repository\'s documentation. What would you like to know?');
            }
            if (isOpen) { input.focus(); }
        });

        clearBtn.addEventListener('click', function () {
            messages.innerHTML = '';
            // Also clear server-side history
            fetch('/api/chat/' + JOB_ID + '/history?session_id=' + SESSION_ID, { method: 'DELETE' });
            appendBubble('assistant', 'Chat history cleared. Ask me anything about the documentation!');
        });

        // Auto-resize textarea
        input.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Send on Enter (Shift+Enter for newline)
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        sendBtn.addEventListener('click', sendMessage);

        function sendMessage() {
            var text = input.value.trim();
            if (!text || isStreaming) return;

            appendBubble('user', escapeHtml(text));
            input.value = '';
            input.style.height = 'auto';
            setStreaming(true);

            var assistantBubble = appendBubble('assistant', '');
            var typingIndicator = document.createElement('span');
            typingIndicator.className = 'chat-typing';
            typingIndicator.textContent = '…';
            assistantBubble.appendChild(typingIndicator);
            scrollToBottom();

            fetch('/api/chat/' + JOB_ID, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, session_id: SESSION_ID })
            }).then(function (resp) {
                if (!resp.ok) {
                    typingIndicator.remove();
                    assistantBubble.textContent = '⚠️ Server error (' + resp.status + '). Please try again.';
                    setStreaming(false);
                    return;
                }
                var reader = resp.body.getReader();
                var decoder = new TextDecoder();
                var rawText = '';
                var buffer = '';

                function pump() {
                    reader.read().then(function (result) {
                        if (result.done) {
                            setStreaming(false);
                            return;
                        }
                        buffer += decoder.decode(result.value, { stream: true });
                        var lines = buffer.split('\\n');
                        buffer = lines.pop(); // keep incomplete line
                        lines.forEach(function (line) {
                            if (line.startsWith('data: ')) {
                                var data = line.slice(6);
                                if (data === '[DONE]') {
                                    setStreaming(false);
                                    return;
                                }
                                // Unescape newlines encoded by the server
                                rawText += data.replace(/\\\\n/g, '\\n');
                                typingIndicator.remove();
                                assistantBubble.innerHTML = renderMarkdown(rawText);
                                scrollToBottom();
                            }
                        });
                        pump();
                    }).catch(function () {
                        setStreaming(false);
                    });
                }
                pump();
            }).catch(function () {
                typingIndicator.remove();
                assistantBubble.textContent = '⚠️ Network error. Please check your connection.';
                setStreaming(false);
            });
        }

        function appendBubble(role, html) {
            var div = document.createElement('div');
            div.className = 'chat-bubble ' + role;
            div.innerHTML = html;
            messages.appendChild(div);
            scrollToBottom();
            return div;
        }

        function scrollToBottom() {
            messages.scrollTop = messages.scrollHeight;
        }

        function setStreaming(val) {
            isStreaming = val;
            sendBtn.disabled = val;
            input.disabled = val;
        }

        function escapeHtml(str) {
            return str
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
        }

        /**
         * Minimal markdown-to-HTML renderer for assistant responses.
         * Handles: code blocks, inline code, bold, italic, links, line breaks.
         */
        function renderMarkdown(md) {
            var html = escapeHtml(md);
            // Fenced code blocks: ```lang\n...\n```
            html = html.replace(/```([^\\n]*)\\n([\\s\\S]*?)```/g, function (_, lang, code) {
                return '<pre><code>' + code + '</code></pre>';
            });
            // Inline code
            html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
            // Bold **text**
            html = html.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>');
            // Italic *text*
            html = html.replace(/\\*([^*]+)\\*/g, '<em>$1</em>');
            // Links [text](url)
            html = html.replace(/\\[([^\\]]+)\\]\\((https?:\\/\\/[^)]+)\\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
            // Headings # / ## / ###
            html = html.replace(/^### (.+)$/gm, '<strong>$1</strong>');
            html = html.replace(/^## (.+)$/gm, '<strong>$1</strong>');
            html = html.replace(/^# (.+)$/gm, '<strong>$1</strong>');
            // Newlines -> <br> (outside pre blocks)
            html = html.replace(/\\n/g, '<br>');
            return html;
        }
    })();
    </script>
</body>
</html>
"""