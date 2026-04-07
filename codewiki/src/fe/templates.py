#!/usr/bin/env python3
"""
HTML templates for the CodeWiki web application.
"""

# Web interface HTML template
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeWiki - GitHub Repository Documentation Generator</title>
    <style>
        /* ── Design tokens ─────────────────────────────────── */
        :root {
            --bg:           #f0f4ff;
            --surface:      #ffffff;
            --surface-2:    #f1f5f9;
            --border:       #e2e8f0;
            --text:         #1e293b;
            --text-muted:   #64748b;
            --primary:      #6366f1;
            --primary-dark: #4f46e5;
            --primary-glow: rgba(99,102,241,.25);
            --success:      #10b981;
            --success-bg:   #d1fae5;
            --success-text: #065f46;
            --error:        #ef4444;
            --error-bg:     #fee2e2;
            --error-text:   #991b1b;
            --warning-bg:   #fef3c7;
            --warning-text: #92400e;
            --info-bg:      #dbeafe;
            --info-text:    #1e40af;
            --radius:       12px;
            --shadow:       0 4px 24px rgba(0,0,0,.08);
            --shadow-lg:    0 20px 48px rgba(0,0,0,.14);
            --transition:   .2s cubic-bezier(.4,0,.2,1);
            /* ── Glass morphism ── */
            --glass-bg:     rgba(255,255,255,.70);
            --glass-border: rgba(255,255,255,.50);
            --glass-blur:   blur(18px) saturate(180%);
            /* ── Background orbs ── */
            --blob-1:       rgba(99,102,241,.18);
            --blob-2:       rgba(6,182,212,.14);
            --blob-3:       rgba(139,92,246,.12);
        }
        [data-theme="dark"] {
            --bg:           #070d1f;
            --surface:      #1e293b;
            --surface-2:    #0f172a;
            --border:       #334155;
            --text:         #f1f5f9;
            --text-muted:   #94a3b8;
            --primary-glow: rgba(99,102,241,.35);
            --success-bg:   #064e3b;
            --success-text: #6ee7b7;
            --error-bg:     #450a0a;
            --error-text:   #fca5a5;
            --warning-bg:   #451a03;
            --warning-text: #fcd34d;
            --info-bg:      #1e3a5f;
            --info-text:    #93c5fd;
            --shadow:       0 4px 24px rgba(0,0,0,.4);
            --shadow-lg:    0 20px 48px rgba(0,0,0,.6);
            /* ── Glass morphism dark ── */
            --glass-bg:     rgba(15,23,42,.72);
            --glass-border: rgba(255,255,255,.08);
            /* ── Background orbs dark ── */
            --blob-1:       rgba(99,102,241,.30);
            --blob-2:       rgba(6,182,212,.22);
            --blob-3:       rgba(139,92,246,.22);
        }

        /* ── Reset ─────────────────────────────────────────── */
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

        /* ── Base ──────────────────────────────────────────── */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--text);
            background-color: var(--bg);
            /* Ambient gradient orbs fixed to viewport */
            background-image:
                radial-gradient(ellipse 60% 50% at 15% 25%,  var(--blob-1) 0%, transparent 60%),
                radial-gradient(ellipse 55% 50% at 85% 75%,  var(--blob-2) 0%, transparent 60%),
                radial-gradient(ellipse 45% 45% at 55% 55%,  var(--blob-3) 0%, transparent 55%);
            background-attachment: fixed;
            min-height: 100vh;
            transition: background-color var(--transition), color var(--transition);
        }

        /* ── Keyframe animations ───────────────────────────── */
        @keyframes fadeIn   { from{opacity:0} to{opacity:1} }
        @keyframes slideUp  { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
        @keyframes slideIn  { from{opacity:0;transform:translateX(-20px)} to{opacity:1;transform:translateX(0)} }
        @keyframes pulse    { 0%,100%{opacity:1} 50%{opacity:.5} }
        @keyframes spin     { to{transform:rotate(360deg)} }
        @keyframes shimmer  {
            0%   { background-position: -400px 0 }
            100% { background-position:  400px 0 }
        }
        @keyframes bounceIn {
            0%   { opacity:0; transform:scale(.85) }
            60%  { opacity:1; transform:scale(1.04) }
            100% { transform:scale(1) }
        }
        @keyframes gradientShift {
            0%,100% { background-position: 0% 50% }
            50%     { background-position: 100% 50% }
        }
        /* Rainbow border spin — uses CSS @property if supported */
        @property --rainbow-angle {
            syntax: '<angle>';
            initial-value: 0deg;
            inherits: false;
        }
        @keyframes rainbowSpin {
            to { --rainbow-angle: 360deg; }
        }

        /* ── Navigation bar ────────────────────────────────── */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            height: 60px;
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border-bottom: 1px solid var(--glass-border);
            box-shadow: 0 1px 16px rgba(0,0,0,.08);
            animation: slideIn .4s ease both;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: .5rem;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary);
            text-decoration: none;
        }
        .navbar-brand span { font-size: 1.4rem; }
        .navbar-actions { display: flex; gap: .75rem; align-items: center; }

        /* ── Theme toggle ──────────────────────────────────── */
        .theme-toggle {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 50px;
            padding: .35rem .75rem;
            cursor: pointer;
            font-size: .85rem;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: .4rem;
            transition: all var(--transition);
        }
        .theme-toggle:hover {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
            transform: translateY(-1px);
        }

        /* ── Hero ──────────────────────────────────────────── */
        .hero {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            background-size: 200% 200%;
            animation: gradientShift 8s ease infinite;
            color: #fff;
            padding: 4rem 2rem 5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: '';
            position: absolute;
            inset: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }
        .hero-icon {
            font-size: 3.5rem;
            display: block;
            margin-bottom: .5rem;
            animation: bounceIn .8s ease both;
        }
        .hero h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            letter-spacing: -.02em;
            margin-bottom: .75rem;
            animation: slideUp .6s .1s ease both;
        }
        .hero p {
            font-size: 1.1rem;
            opacity: .9;
            max-width: 480px;
            margin: 0 auto;
            animation: slideUp .6s .2s ease both;
        }

        /* ── Wave divider ──────────────────────────────────── */
        .wave {
            display: block;
            margin-top: -2px;
            fill: var(--bg);
            transition: fill var(--transition);
        }

        /* ── Main layout ───────────────────────────────────── */
        .main { max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }

        /* ── Card ──────────────────────────────────────────── */
        .card {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,.35);
            padding: 2rem;
            margin-bottom: 2rem;
            animation: slideUp .5s ease both;
            transition: background var(--transition), border-color var(--transition), box-shadow var(--transition);
        }
        .card:hover {
            box-shadow: var(--shadow-lg), inset 0 1px 0 rgba(255,255,255,.4);
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: .5rem;
        }

        /* ── Form ──────────────────────────────────────────── */
        .form-group { margin-bottom: 1.5rem; }
        .form-group label {
            display: block;
            margin-bottom: .5rem;
            font-weight: 600;
            font-size: .9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: .04em;
        }
        .input-wrapper {
            position: relative;
            isolation: isolate;
        }
        .input-wrapper .input-icon {
            position: absolute;
            left: .9rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1rem;
            pointer-events: none;
            z-index: 2;
        }
        /* Rainbow rotating ring shown on focus */
        .input-wrapper::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 13px;
            background: conic-gradient(
                from var(--rainbow-angle),
                #ff0080, #ff4500, #ffcc00, #39ff14, #00cfff, #7b2ff7, #ff0080
            );
            animation: rainbowSpin 2.5s linear infinite paused;
            opacity: 0;
            transition: opacity .3s ease;
            z-index: 0;
        }
        .input-wrapper:focus-within::before {
            opacity: 1;
            animation-play-state: running;
        }
        .form-group input {
            position: relative;
            z-index: 1;
            width: 100%;
            padding: .85rem 1rem .85rem 2.6rem;
            border: 2px solid var(--border);
            border-radius: 10px;
            font-size: 1rem;
            background: var(--glass-bg);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            color: var(--text);
            transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
        }
        .form-group input:focus {
            outline: none;
            border-color: transparent;
            box-shadow: 0 0 0 2px var(--primary-glow);
            background: var(--glass-bg);
        }
        .input-hint {
            margin-top: .4rem;
            font-size: .8rem;
            color: var(--text-muted);
        }
        .input-error { color: var(--error); display: none; }
        .input-error.visible { display: block; }

        /* ── Button ────────────────────────────────────────── */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: .5rem;
            padding: .85rem 2rem;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all var(--transition);
            position: relative;
            overflow: hidden;
        }
        .btn::after {
            content:'';
            position:absolute;
            inset:0;
            background: rgba(255,255,255,.15);
            opacity:0;
            transition: opacity var(--transition);
        }
        .btn:hover::after { opacity:1; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px var(--primary-glow); }
        .btn:active { transform: translateY(0); }
        .btn:disabled {
            background: var(--text-muted);
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .btn-sm { padding: .5rem 1.1rem; font-size: .85rem; border-radius: 8px; }
        .btn-outline {
            background: rgba(99,102,241,.08);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 2px solid var(--primary);
            color: var(--primary);
        }
        .btn-outline:hover { background: var(--primary); color: #fff; }
        .btn-full { width: 100%; }

        /* ── Rainbow wrap — surrounds a button with rotating rainbow border ── */
        .rainbow-wrap {
            display: block;
            position: relative;
            border-radius: 12px;
            isolation: isolate;
        }
        .rainbow-wrap::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 13px;
            background: conic-gradient(
                from var(--rainbow-angle),
                #ff0080, #ff4500, #ffcc00, #39ff14, #00cfff, #7b2ff7, #ff0080
            );
            animation: rainbowSpin 2.5s linear infinite paused;
            opacity: 0;
            transition: opacity .35s ease;
            z-index: -1;
        }
        .rainbow-wrap:hover::before,
        .rainbow-wrap:focus-within::before {
            opacity: 1;
            animation-play-state: running;
        }

        /* spinner inside button */
        .spinner {
            width: 16px; height: 16px;
            border: 2px solid rgba(255,255,255,.4);
            border-top-color: #fff;
            border-radius: 50%;
            animation: spin .7s linear infinite;
            display: none;
        }
        .btn.loading .spinner { display: block; }
        .btn.loading .btn-label { opacity: .6; }

        /* ── Alert ─────────────────────────────────────────── */
        .alert {
            padding: 1rem 1.25rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: flex-start;
            gap: .75rem;
            animation: slideUp .35s ease both;
            font-size: .95rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        .alert-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: .05rem; }
        .alert-success { background: rgba(209,250,229,.75); color: var(--success-text); border: 1px solid rgba(110,231,183,.5); }
        .alert-error   { background: rgba(254,226,226,.75); color: var(--error-text);   border: 1px solid rgba(252,165,165,.5); }

        /* ── Section title ─────────────────────────────────── */
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }
        .section-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: .5rem;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            padding: .15rem .55rem;
            border-radius: 99px;
            font-size: .75rem;
            font-weight: 600;
        }
        .badge-primary { background: var(--info-bg); color: var(--info-text); }

        /* ── Job card ──────────────────────────────────────── */
        .job-card {
            background: rgba(255,255,255,.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,.35);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin-bottom: .85rem;
            animation: slideIn .4s ease both;
            transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
        }
        [data-theme="dark"] .job-card {
            background: rgba(15,23,42,.55);
            border-color: rgba(255,255,255,.06);
        }
        .job-card:hover {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow), 0 8px 24px rgba(0,0,0,.12);
        }
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: .5rem;
        }
        .job-url {
            font-weight: 600;
            color: var(--primary);
            font-size: .9rem;
            word-break: break-all;
        }
        .job-status {
            padding: .2rem .65rem;
            border-radius: 99px;
            font-size: .75rem;
            font-weight: 700;
            white-space: nowrap;
            flex-shrink: 0;
        }
        .status-queued     { background: var(--warning-bg); color: var(--warning-text); }
        .status-processing { background: var(--info-bg);    color: var(--info-text); animation: pulse 1.5s ease infinite; }
        .status-completed  { background: var(--success-bg); color: var(--success-text); }
        .status-failed     { background: var(--error-bg);   color: var(--error-text); }
        .job-progress {
            font-size: .82rem;
            color: var(--text-muted);
            margin-bottom: .6rem;
            display: flex;
            align-items: center;
            gap: .4rem;
        }
        .job-progress-dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: var(--text-muted);
            flex-shrink: 0;
        }
        .status-processing ~ .job-progress .job-progress-dot {
            background: var(--primary);
            animation: pulse 1s ease infinite;
        }
        .job-meta {
            font-size: .75rem;
            color: var(--text-muted);
            margin-bottom: .6rem;
        }
        .job-footer {
            display: flex;
            gap: .6rem;
            flex-wrap: wrap;
            margin-top: .5rem;
        }

        /* ── Progress bar ──────────────────────────────────── */
        .progress-bar-wrap {
            height: 4px;
            background: var(--border);
            border-radius: 2px;
            overflow: hidden;
            margin: .5rem 0 .75rem;
        }
        .progress-bar {
            height: 100%;
            border-radius: 2px;
            background: linear-gradient(90deg, var(--primary), #06b6d4);
            background-size: 200% 100%;
            animation: shimmer 1.5s linear infinite;
            transition: width .4s ease;
        }

        /* ── Footer ────────────────────────────────────────── */
        footer {
            text-align: center;
            padding: 2rem 1rem;
            font-size: .82rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border);
        }
        footer a { color: var(--primary); text-decoration: none; }
        footer a:hover { text-decoration: underline; }

        /* ── Responsive ────────────────────────────────────── */
        @media (max-width: 600px) {
            .hero { padding: 2.5rem 1rem 3rem; }
            .card { padding: 1.25rem; }
            .job-header { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <!-- ── Nav ──────────────────────────────────────────── -->
    <nav class="navbar">
        <a href="/" class="navbar-brand">
            <span>📚</span> CodeWiki
        </a>
        <div class="navbar-actions">
            <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
                <span id="themeIcon">🌙</span>
                <span id="themeLabel">Dark</span>
            </button>
        </div>
    </nav>

    <!-- ── Hero ─────────────────────────────────────────── -->
    <section class="hero">
        <span class="hero-icon">📖</span>
        <h1>Instant Code Documentation</h1>
        <p>Paste any GitHub repository URL and let AI generate beautiful, structured docs in seconds.</p>
    </section>
    <svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" class="wave" preserveAspectRatio="none" style="width:100%;margin-top:-1px;">
        <path d="M0,48 C360,0 1080,0 1440,48 L1440,48 L0,48 Z"/>
    </svg>

    <!-- ── Main ─────────────────────────────────────────── -->
    <main class="main">

        <!-- Alert -->
        {% if message %}
        <div class="alert alert-{{ message_type }}" role="alert">
            <span class="alert-icon">{% if message_type == 'success' %}✅{% else %}❌{% endif %}</span>
            <span>{{ message }}</span>
        </div>
        {% endif %}

        <!-- Submit form -->
        <div class="card" style="animation-delay:.05s">
            <div class="card-title">🚀 Generate Documentation</div>
            <form method="POST" action="/" id="submitForm" novalidate>
                <div class="form-group">
                    <label for="repo_url">GitHub Repository URL</label>
                    <div class="input-wrapper">
                        <span class="input-icon">🔗</span>
                        <input
                            type="url"
                            id="repo_url"
                            name="repo_url"
                            placeholder="https://github.com/owner/repository"
                            required
                            value="{{ repo_url or '' }}"
                            autocomplete="url"
                        >
                    </div>
                    <p class="input-hint input-error" id="urlError">Please enter a valid GitHub URL (https://github.com/owner/repo)</p>
                </div>

                <div class="form-group">
                    <label for="commit_id">Specific Commit <span style="font-weight:400;text-transform:none;font-size:.8rem">(optional)</span></label>
                    <div class="input-wrapper">
                        <span class="input-icon">🔖</span>
                        <input
                            type="text"
                            id="commit_id"
                            name="commit_id"
                            placeholder="Commit SHA — leave blank for latest"
                            value="{{ commit_id or '' }}"
                            pattern="[a-fA-F0-9]{4,40}"
                            title="4–40 hexadecimal characters (0-9, a-f, case-insensitive)"
                        >
                    </div>
                    <p class="input-hint">Leave empty to use the repository's latest commit.</p>
                </div>

                <div class="rainbow-wrap">
                <button type="submit" class="btn btn-full" id="submitBtn">
                    <div class="spinner" id="spinner"></div>
                    <span class="btn-label" id="btnLabel">⚡ Generate Documentation</span>
                </button>
                </div>
            </form>
        </div>

        <!-- Recent jobs -->
        {% if recent_jobs %}
        <div class="card" style="animation-delay:.15s">
            <div class="section-header">
                <span class="section-title">🕒 Recent Jobs <span class="badge badge-primary" id="jobCount">{{ recent_jobs | length }}</span></span>
                <button class="btn btn-sm btn-outline" onclick="window.location.reload()" title="Refresh job list">↻ Refresh</button>
            </div>

            <div id="jobsList">
            {% for job in recent_jobs %}
            <div class="job-card" id="job-{{ job.job_id }}" style="animation-delay:{{ loop.index0 * 0.06 }}s">
                <div class="job-header">
                    <span class="job-url">{{ job.repo_url }}</span>
                    <span class="job-status status-{{ job.status }}">{{ job.status | upper }}</span>
                </div>
                {% if job.status in ['queued', 'processing'] %}
                <div class="progress-bar-wrap">
                    <div class="progress-bar" style="width:{% if job.status == 'queued' %}15{% else %}60{% endif %}%"></div>
                </div>
                {% endif %}
                <div class="job-progress">
                    <span class="job-progress-dot"></span>
                    <span>{{ job.progress or 'Waiting…' }}</span>
                </div>
                {% if job.main_model %}
                <div class="job-meta">🤖 Model: {{ job.main_model }}</div>
                {% endif %}
                {% if job.commit_id %}
                <div class="job-meta">🔖 Commit: <code>{{ job.commit_id[:8] }}</code></div>
                {% endif %}
                <div class="job-footer">
                    {% if job.status == 'completed' %}
                    <a href="/docs/{{ job.job_id }}" class="btn btn-sm">📄 View Docs</a>
                    {% endif %}
                    <a href="/api/job/{{ job.job_id }}" class="btn btn-sm btn-outline" target="_blank">🔍 JSON</a>
                </div>
            </div>
            {% endfor %}
            </div>
        </div>
        {% endif %}
    </main>

    <!-- ── Footer ────────────────────────────────────────── -->
    <footer>
        <p>CodeWiki &mdash; AI-powered documentation generator &bull;
           <a href="https://github.com/WebCafeTech/AutoCodeWikiAI" target="_blank" rel="noopener">GitHub</a>
        </p>
    </footer>

    <script>
    /* ── Theme toggle ─────────────────────────────────── */
    (function(){
        const root  = document.documentElement;
        const btn   = document.getElementById('themeToggle');
        const icon  = document.getElementById('themeIcon');
        const label = document.getElementById('themeLabel');
        const stored = localStorage.getItem('cw-theme');
        if (stored) { root.dataset.theme = stored; }
        function apply(theme) {
            root.dataset.theme = theme;
            icon.textContent  = theme === 'dark' ? '☀️' : '🌙';
            label.textContent = theme === 'dark' ? 'Light' : 'Dark';
            localStorage.setItem('cw-theme', theme);
        }
        apply(root.dataset.theme || 'light');
        btn.addEventListener('click', () => apply(root.dataset.theme === 'dark' ? 'light' : 'dark'));
    })();

    /* ── Form validation & submit animation ──────────── */
    (function(){
        const form   = document.getElementById('submitForm');
        const urlIn  = document.getElementById('repo_url');
        const urlErr = document.getElementById('urlError');
        const btn    = document.getElementById('submitBtn');
        const lbl    = document.getElementById('btnLabel');
        let busy = false;

        function isGithubUrl(v) {
            return /^https?:\\/\\/github\\.com\\/[^/]+\\/[^/]+/.test(v.trim());
        }

        urlIn.addEventListener('input', function() {
            if (this.value && !isGithubUrl(this.value)) {
                urlErr.classList.add('visible');
                this.style.borderColor = 'var(--error)';
            } else {
                urlErr.classList.remove('visible');
                this.style.borderColor = '';
            }
        });

        form.addEventListener('submit', function(e) {
            if (!isGithubUrl(urlIn.value)) {
                e.preventDefault();
                urlErr.classList.add('visible');
                urlIn.focus();
                return;
            }
            if (busy) { e.preventDefault(); return; }
            busy = true;
            btn.classList.add('loading');
            btn.disabled = true;
            lbl.textContent = 'Generating…';
            setTimeout(() => {
                busy = false;
                btn.classList.remove('loading');
                btn.disabled = false;
                lbl.textContent = '⚡ Generate Documentation';
            }, 12000);
        });
    })();

    /* ── Live job polling ────────────────────────────── */
    (function(){
        const INTERVAL = 5000;
        function activeJobIds() {
            return Array.from(document.querySelectorAll('.job-card'))
                .filter(el => el.querySelector('.status-queued, .status-processing'))
                .map(el => el.id.replace('job-',''));
        }

        async function pollJob(jobId) {
            try {
                const res = await fetch('/api/job/' + jobId);
                if (!res.ok) return;
                const data = await res.json();
                const card = document.getElementById('job-' + jobId);
                if (!card) return;

                // Update status badge
                const badge = card.querySelector('.job-status');
                if (badge) {
                    badge.textContent = (data.status || '').toUpperCase();
                    badge.className = 'job-status status-' + data.status;
                }

                // Update progress text
                const prog = card.querySelector('.job-progress span:last-child');
                if (prog) prog.textContent = data.progress || 'Waiting…';

                // Update progress bar (queued=15%, processing=60%, completed=100%)
                const bar = card.querySelector('.progress-bar');
                if (bar) {
                    const WIDTH = { queued: '15%', processing: '60%', completed: '100%' };
                    if (WIDTH[data.status]) bar.style.width = WIDTH[data.status];
                }

                // Show docs link on completion
                if (data.status === 'completed') {
                    const footer = card.querySelector('.job-footer');
                    if (footer && !footer.querySelector('a[href*="/docs/"]')) {
                        const a = document.createElement('a');
                        a.href = '/docs/' + jobId;
                        a.className = 'btn btn-sm';
                        a.textContent = '📄 View Docs';
                        footer.insertBefore(a, footer.firstChild);
                    }
                    const pbWrap = card.querySelector('.progress-bar-wrap');
                    if (pbWrap) pbWrap.remove();
                }
            } catch(_) {}
        }

        function tick() {
            const ids = activeJobIds();
            ids.forEach(pollJob);
            if (ids.length > 0) setTimeout(tick, INTERVAL);
        }

        if (activeJobIds().length > 0) setTimeout(tick, INTERVAL);
    })();
    </script>
</body>
</html>
"""

# HTML template for the documentation pages
DOCS_VIEW_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} — CodeWiki</title>
    <!-- Mermaid -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.9.0/dist/mermaid.min.js"></script>
    <!-- Highlight.js for syntax highlighting -->
    <link rel="stylesheet" id="hljs-light" href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/github.min.css">
    <link rel="stylesheet" id="hljs-dark"  href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/github-dark.min.css" disabled>
    <script src="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/highlight.min.js"></script>
    <style>
        /* ── Design tokens ─────────────────────────────────── */
        :root {
            --bg:           #f0f4ff;
            --surface:      #ffffff;
            --surface-2:    #f1f5f9;
            --border:       #e2e8f0;
            --text:         #1e293b;
            --text-muted:   #64748b;
            --primary:      #6366f1;
            --primary-dark: #4f46e5;
            --primary-glow: rgba(99,102,241,.2);
            --code-bg:      #f1f5f9;
            --pre-bg:       #f8fafc;
            --transition:   .2s cubic-bezier(.4,0,.2,1);
            --sidebar-w:    280px;
            /* ── Glass morphism ── */
            --glass-bg:     rgba(255,255,255,.70);
            --glass-border: rgba(255,255,255,.50);
            --glass-blur:   blur(18px) saturate(180%);
            /* ── Background orbs ── */
            --blob-1:       rgba(99,102,241,.15);
            --blob-2:       rgba(6,182,212,.12);
            --blob-3:       rgba(139,92,246,.10);
        }
        [data-theme="dark"] {
            --bg:           #070d1f;
            --surface:      #1e293b;
            --surface-2:    #0f172a;
            --border:       #334155;
            --text:         #e2e8f0;
            --text-muted:   #94a3b8;
            --code-bg:      #1e293b;
            --pre-bg:       #0f172a;
            /* ── Glass morphism dark ── */
            --glass-bg:     rgba(15,23,42,.72);
            --glass-border: rgba(255,255,255,.08);
            /* ── Background orbs dark ── */
            --blob-1:       rgba(99,102,241,.28);
            --blob-2:       rgba(6,182,212,.20);
            --blob-3:       rgba(139,92,246,.20);
        }

        /* ── Reset ─────────────────────────────────────────── */
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

        /* ── Animations ────────────────────────────────────── */
        @keyframes fadeIn  { from{opacity:0} to{opacity:1} }
        @keyframes slideIn { from{opacity:0;transform:translateX(-16px)} to{opacity:1;transform:translateX(0)} }
        @keyframes slideUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @property --rainbow-angle {
            syntax: '<angle>';
            initial-value: 0deg;
            inherits: false;
        }
        @keyframes rainbowSpin {
            to { --rainbow-angle: 360deg; }
        }

        /* ── Base ──────────────────────────────────────────── */
        html { scroll-behavior: smooth; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
            line-height: 1.7;
            color: var(--text);
            background-color: var(--bg);
            background-image:
                radial-gradient(ellipse 60% 50% at 10% 20%, var(--blob-1) 0%, transparent 60%),
                radial-gradient(ellipse 50% 50% at 90% 80%, var(--blob-2) 0%, transparent 60%),
                radial-gradient(ellipse 45% 45% at 55% 50%, var(--blob-3) 0%, transparent 55%);
            background-attachment: fixed;
            transition: background-color var(--transition), color var(--transition);
        }

        /* ── Top bar ───────────────────────────────────────── */
        .topbar {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 200;
            height: 56px;
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0 1rem;
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border-bottom: 1px solid var(--glass-border);
            box-shadow: 0 1px 16px rgba(0,0,0,.08);
            transition: background var(--transition), border-color var(--transition);
        }
        .topbar-brand {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--primary);
            text-decoration: none;
            white-space: nowrap;
        }
        .topbar-sep { color: var(--border); font-size: 1.4rem; }
        .topbar-title {
            font-size: .95rem;
            color: var(--text-muted);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            flex: 1;
        }
        .topbar-actions { display: flex; gap: .6rem; flex-shrink: 0; }
        .icon-btn {
            background: rgba(255,255,255,.35);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,.4);
            border-radius: 8px;
            padding: .35rem .65rem;
            cursor: pointer;
            font-size: .85rem;
            color: var(--text);
            display: flex; align-items: center; gap: .3rem;
            transition: all var(--transition);
            white-space: nowrap;
            position: relative;
            isolation: isolate;
        }
        [data-theme="dark"] .icon-btn {
            background: rgba(15,23,42,.50);
            border-color: rgba(255,255,255,.10);
        }
        /* Rainbow ring on hover / focus */
        .icon-btn::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 10px;
            background: conic-gradient(
                from var(--rainbow-angle),
                #ff0080, #ff4500, #ffcc00, #39ff14, #00cfff, #7b2ff7, #ff0080
            );
            animation: rainbowSpin 2.5s linear infinite paused;
            opacity: 0;
            transition: opacity .3s ease;
            z-index: -1;
        }
        .icon-btn:hover::before,
        .icon-btn:focus::before {
            opacity: 1;
            animation-play-state: running;
        }
        .icon-btn:hover { background: var(--primary); color: #fff; border-color: transparent; }

        /* ── Layout ────────────────────────────────────────── */
        .layout {
            display: flex;
            padding-top: 56px;
            min-height: 100vh;
        }

        /* ── Sidebar ───────────────────────────────────────── */
        .sidebar {
            width: var(--sidebar-w);
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border-right: 1px solid var(--glass-border);
            position: fixed;
            top: 56px;
            left: 0;
            bottom: 0;
            overflow-y: auto;
            padding: 1.25rem 1rem;
            transition: transform var(--transition), background var(--transition), border-color var(--transition);
            animation: slideIn .4s ease both;
            z-index: 100;
        }
        .sidebar::-webkit-scrollbar { width: 4px; }
        .sidebar::-webkit-scrollbar-track { background: transparent; }
        .sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

        /* ── Nav items ─────────────────────────────────────── */
        .nav-group { margin-bottom: 1.25rem; }
        .nav-group-toggle {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: .35rem .6rem;
            font-size: .72rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: .07em;
            cursor: pointer;
            border-radius: 6px;
            user-select: none;
            transition: background var(--transition);
        }
        .nav-group-toggle:hover { background: var(--surface-2); }
        .nav-group-toggle .chevron {
            transition: transform var(--transition);
            font-style: normal;
        }
        .nav-group.collapsed .chevron { transform: rotate(-90deg); }
        .nav-group.collapsed .nav-group-items { display: none; }
        .nav-item {
            display: block;
            padding: .45rem .75rem;
            color: var(--text-muted);
            text-decoration: none;
            border-radius: 7px;
            font-size: .85rem;
            transition: all var(--transition);
            margin-bottom: 2px;
        }
        .nav-item:hover { background: var(--surface-2); color: var(--text); }
        .nav-item.active {
            background: var(--primary-glow);
            color: var(--primary);
            font-weight: 600;
        }
        .nav-subsection { margin-left: 12px; }
        .nav-subsection .nav-item { font-size: .8rem; }
        .nav-subsection .nav-subsection { margin-left: 10px; }
        .nav-subsection .nav-subsection .nav-item { font-size: .75rem; }
        .nav-section-header {
            padding: .35rem .6rem;
            font-size: .78rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 2px;
        }

        /* ── Generation info badge ─────────────────────────── */
        .gen-info {
            background: rgba(255,255,255,.45);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,.35);
            border-radius: 8px;
            padding: .75rem;
            margin-bottom: 1.25rem;
            font-size: .75rem;
            color: var(--text-muted);
            line-height: 1.5;
        }
        [data-theme="dark"] .gen-info {
            background: rgba(15,23,42,.55);
            border-color: rgba(255,255,255,.06);
        }
        .gen-info-title {
            font-size: .68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .07em;
            color: var(--text-muted);
            margin-bottom: .5rem;
        }
        .gen-info-row { margin-bottom: .2rem; }
        .gen-info-row strong { color: var(--text); }

        /* ── Main content ──────────────────────────────────── */
        .main-content {
            flex: 1;
            margin-left: var(--sidebar-w);
            padding: 2.5rem 3rem 4rem;
            max-width: 100%;
            animation: slideUp .45s ease both;
            transition: margin var(--transition);
        }
        .markdown-content { max-width: 860px; }

        /* ── Markdown typography ───────────────────────────── */
        .markdown-content h1 {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text);
            margin-bottom: 1rem;
            padding-bottom: .6rem;
            border-bottom: 2px solid var(--border);
            animation: fadeIn .5s ease both;
        }
        .markdown-content h2 {
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text);
            margin: 2.5rem 0 .85rem;
            padding-bottom: .3rem;
            border-bottom: 1px solid var(--border);
        }
        .markdown-content h3 {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text);
            margin: 1.75rem 0 .65rem;
        }
        .markdown-content h4 {
            font-size: 1.05rem;
            font-weight: 600;
            margin: 1.5rem 0 .5rem;
        }
        .markdown-content p {
            margin-bottom: 1rem;
            color: var(--text);
            line-height: 1.8;
        }
        .markdown-content ul,
        .markdown-content ol {
            margin-bottom: 1rem;
            padding-left: 1.6rem;
        }
        .markdown-content li { margin-bottom: .4rem; color: var(--text); }
        .markdown-content code {
            background: var(--code-bg);
            padding: .15rem .45rem;
            border-radius: .3rem;
            font-family: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
            font-size: .875em;
            color: var(--primary);
            border: 1px solid var(--border);
        }
        .markdown-content pre {
            background: rgba(248,250,252,.75);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,.45);
            border-radius: 10px;
            padding: 1.1rem 1.25rem;
            overflow-x: auto;
            margin-bottom: 1.25rem;
            position: relative;
        }
        [data-theme="dark"] .markdown-content pre {
            background: rgba(15,23,42,.70);
            border-color: rgba(255,255,255,.06);
        }
        .markdown-content pre code {
            background: transparent;
            padding: 0;
            border: none;
            font-size: .875rem;
            color: inherit;
        }
        .copy-btn {
            position: absolute;
            top: .5rem; right: .5rem;
            background: rgba(255,255,255,.7);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,.5);
            border-radius: 6px;
            padding: .2rem .5rem;
            font-size: .7rem;
            cursor: pointer;
            color: var(--text-muted);
            transition: all var(--transition);
            opacity: 0;
        }
        [data-theme="dark"] .copy-btn {
            background: rgba(30,41,59,.8);
            border-color: rgba(255,255,255,.1);
        }
        .markdown-content pre:hover .copy-btn { opacity: 1; }
        .copy-btn:hover { background: var(--primary); color: #fff; border-color: var(--primary); }
        .markdown-content blockquote {
            border-left: 4px solid var(--primary);
            padding: .6rem 1rem;
            margin-bottom: 1rem;
            background: rgba(99,102,241,.06);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            border-radius: 0 8px 8px 0;
            color: var(--text-muted);
            font-style: italic;
        }
        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1.25rem;
            font-size: .9rem;
        }
        .markdown-content th,
        .markdown-content td {
            border: 1px solid var(--border);
            padding: .6rem .85rem;
            text-align: left;
        }
        .markdown-content th {
            background: var(--surface-2);
            font-weight: 600;
        }
        .markdown-content tr:hover td { background: var(--surface-2); }
        .markdown-content a {
            color: var(--primary);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color var(--transition);
        }
        .markdown-content a:hover { border-bottom-color: var(--primary); }

        /* ── Mermaid diagrams ──────────────────────────────── */
        .mermaid {
            background: rgba(255,255,255,.55);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,.4);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1.25rem 0;
            overflow-x: auto;
            text-align: center;
        }
        [data-theme="dark"] .mermaid {
            background: rgba(15,23,42,.55);
            border-color: rgba(255,255,255,.06);
        }

        /* ── Mobile ────────────────────────────────────────── */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
            }
            .sidebar.open {
                transform: translateX(0);
                box-shadow: 4px 0 24px rgba(0,0,0,.15);
            }
            .main-content {
                margin-left: 0;
                padding: 1.5rem 1.1rem 3rem;
            }
            .topbar-title { display: none; }
        }

        /* ── Overlay ───────────────────────────────────────── */
        .sidebar-overlay {
            display: none;
            position: fixed;
            inset: 56px 0 0 0;
            background: rgba(0,0,0,.4);
            z-index: 99;
        }
        .sidebar-overlay.visible { display: block; }
    </style>
</head>
<body>
    <!-- ── Top bar ─────────────────────────────────────────── -->
    <header class="topbar">
        <button class="icon-btn" id="sidebarToggle" aria-label="Toggle sidebar">☰</button>
        <a href="/" class="topbar-brand">📚 CodeWiki</a>
        <span class="topbar-sep">/</span>
        <span class="topbar-title">{{ repo_name }} — {{ title }}</span>
        <div class="topbar-actions">
            <a href="/" class="icon-btn">← Home</a>
            <button class="icon-btn" id="themeToggle" aria-label="Toggle theme">
                <span id="themeIcon">🌙</span>
                <span id="themeLabel">Dark</span>
            </button>
        </div>
    </header>

    <div class="sidebar-overlay" id="sidebarOverlay"></div>

    <div class="layout">
        <!-- ── Sidebar ──────────────────────────────────────── -->
        <nav class="sidebar" id="sidebar">
            {% if metadata and metadata.generation_info %}
            <div class="gen-info">
                <div class="gen-info-title">⚙ Generation Info</div>
                <div class="gen-info-row"><strong>Model:</strong> {{ metadata.generation_info.main_model }}</div>
                <div class="gen-info-row"><strong>Generated:</strong> {{ metadata.generation_info.timestamp[:16] }}</div>
                {% if metadata.generation_info.commit_id %}
                <div class="gen-info-row"><strong>Commit:</strong> <code>{{ metadata.generation_info.commit_id[:8] }}</code></div>
                {% endif %}
                {% if metadata.statistics %}
                <div class="gen-info-row"><strong>Components:</strong> {{ metadata.statistics.total_components }}</div>
                {% endif %}
            </div>
            {% endif %}

            {% if navigation %}
            <div class="nav-group">
                <div class="nav-group-toggle" data-group="overview">
                    <span>📋 Pages</span>
                    <i class="chevron">▾</i>
                </div>
                <div class="nav-group-items">
                    <a href="/static-docs/{{ job_id }}/overview.md"
                       class="nav-item {% if current_page == 'overview.md' %}active{% endif %}">
                        🏠 Overview
                    </a>
                </div>
            </div>

            {% macro render_nav_item(key, data, depth=0) %}
                {% set indent_class = 'nav-subsection' if depth > 0 else '' %}
                <div class="{{ indent_class }}">
                    {% if data.components %}
                        <a href="/static-docs/{{ job_id }}/{{ key }}.md"
                           class="nav-item {% if current_page == key + '.md' %}active{% endif %}">
                            {{ key.replace('_', ' ').title() }}
                        </a>
                    {% else %}
                        <div class="nav-section-header">{{ key.replace('_', ' ').title() }}</div>
                    {% endif %}
                    {% if data.children %}
                        {% for child_key, child_data in data.children.items() %}
                            {{ render_nav_item(child_key, child_data, depth + 1) }}
                        {% endfor %}
                    {% endif %}
                </div>
            {% endmacro %}

            <div class="nav-group" id="modules-group">
                <div class="nav-group-toggle" data-group="modules">
                    <span>🗂 Modules</span>
                    <i class="chevron">▾</i>
                </div>
                <div class="nav-group-items">
                    {% for section_key, section_data in navigation.items() %}
                        {{ render_nav_item(section_key, section_data) }}
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        </nav>

        <!-- ── Main ─────────────────────────────────────────── -->
        <main class="main-content">
            <article class="markdown-content">
                {{ content | safe }}
            </article>
        </main>
    </div>

    <script>
    /* ── Theme toggle ─────────────────────────────────── */
    (function(){
        const root  = document.documentElement;
        const btn   = document.getElementById('themeToggle');
        const icon  = document.getElementById('themeIcon');
        const label = document.getElementById('themeLabel');
        const hlLight = document.getElementById('hljs-light');
        const hlDark  = document.getElementById('hljs-dark');

        function apply(theme) {
            root.dataset.theme = theme;
            icon.textContent  = theme === 'dark' ? '☀️' : '🌙';
            label.textContent = theme === 'dark' ? 'Light' : 'Dark';
            localStorage.setItem('cw-theme', theme);
            if (theme === 'dark') {
                hlLight.disabled = true;
                hlDark.disabled  = false;
            } else {
                hlLight.disabled = false;
                hlDark.disabled  = true;
            }
            // re-render mermaid with matching theme
            if (window.mermaid) {
                mermaid.initialize({
                    startOnLoad: false,
                    theme: theme === 'dark' ? 'dark' : 'default'
                });
                document.querySelectorAll('.mermaid[data-processed]').forEach(el => {
                    el.removeAttribute('data-processed');
                    // data-src was stored via textContent at init time so it contains
                    // plain diagram text, never HTML.  Using textContent (not innerHTML)
                    // means it cannot execute scripts — safe against XSS.
                    const src = el.getAttribute('data-src');
                    if (src) { el.textContent = src; }
                });
                mermaid.init(undefined, document.querySelectorAll('.mermaid'));
            }
        }

        const stored = localStorage.getItem('cw-theme') || 'light';
        apply(stored);
        btn.addEventListener('click', () => apply(root.dataset.theme === 'dark' ? 'light' : 'dark'));
    })();

    /* ── Sidebar toggle ───────────────────────────────── */
    (function(){
        const sidebar  = document.getElementById('sidebar');
        const overlay  = document.getElementById('sidebarOverlay');
        const toggle   = document.getElementById('sidebarToggle');

        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('visible');
        });
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('visible');
        });

        // Collapsible nav groups
        document.querySelectorAll('.nav-group-toggle').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.closest('.nav-group').classList.toggle('collapsed');
            });
        });
    })();

    /* ── Syntax highlighting ──────────────────────────── */
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('pre code:not(.language-mermaid)').forEach(block => {
            hljs.highlightElement(block);

            // Add copy button
            const pre = block.parentElement;
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.textContent = '⎘ Copy';
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(block.innerText).then(() => {
                    copyBtn.textContent = '✓ Copied!';
                    setTimeout(() => { copyBtn.textContent = '⎘ Copy'; }, 1800);
                });
            });
            pre.style.position = 'relative';
            pre.appendChild(copyBtn);
        });
    });

    /* ── Mermaid ──────────────────────────────────────── */
    (function(){
        const isDark = document.documentElement.dataset.theme === 'dark';
        mermaid.initialize({
            startOnLoad: false,
            theme: isDark ? 'dark' : 'default',
            themeVariables: {
                primaryColor: '#6366f1',
                primaryTextColor: '#1e293b',
                primaryBorderColor: '#e2e8f0',
                lineColor: '#64748b',
                secondaryColor: '#f1f5f9',
                tertiaryColor: '#f8fafc'
            },
            flowchart: { htmlLabels: true, curve: 'basis' },
            sequence: { useMaxWidth: true }
        });

        // Store original diagram source as text (safe from XSS when later restored via textContent)
        document.querySelectorAll('.mermaid').forEach(el => {
            el.setAttribute('data-src', el.textContent);
        });

        document.addEventListener('DOMContentLoaded', function() {
            mermaid.init(undefined, document.querySelectorAll('.mermaid'));
        });
    })();
    </script>
</body>
</html>
"""