// ═══════════════════════════════════════════════════════════════
// ENTERPRISE COPILOT · PRODUCTION SCRIPT
// ═══════════════════════════════════════════════════════════════

const chatBox   = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn   = document.getElementById('send-btn');
const progress  = document.querySelector('.progress-fill');

// ── METADATA PARSER ──────────────────────────────────────────────
function parseResponse(rawText) {
    const lines = rawText.split('\n');
    let bodyHtml = '';
    let metaHtml  = '';

    lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed.startsWith('Source:')) {
            const titleMatch = trimmed.match(/\[(.+?)\]/);
            const timeMatch  = trimmed.match(/\((.+?)\)/);
            const title = titleMatch ? titleMatch[1] : 'Video Source';
            const time  = timeMatch  ? timeMatch[1]  : '';
            metaHtml = `
                <div class="source-chip">
                    <span class="src-icon">🎬</span>
                    <span class="src-title">${escHtml(title)}</span>
                    ${time ? `<span class="ts-badge">${escHtml(time)}</span>` : ''}
                </div>`;
        } else if (trimmed.length > 0) {
            bodyHtml += `<p>${escHtml(trimmed)}</p>`;
        }
    });

    return bodyHtml + metaHtml || rawText.replace(/\n/g, '<br>');
}

function escHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

// ── APPEND MESSAGE ROW ────────────────────────────────────────────
function appendMessage(role, contentHtml, isRaw = false) {
    const row = document.createElement('div');
    row.classList.add('message-row', role === 'user' ? 'user-row' : 'ai-row');

    const avatar = document.createElement('div');
    avatar.classList.add('msg-avatar', role === 'user' ? 'user-avatar' : 'ai-avatar');
    avatar.textContent = role === 'user' ? 'YOU' : 'AI';

    const bubble = document.createElement('div');
    bubble.classList.add('msg-bubble', role === 'user' ? 'user-bubble' : 'ai-bubble');

    if (isRaw) {
        bubble.innerHTML = contentHtml;
    } else if (role === 'ai') {
        bubble.innerHTML = parseResponse(contentHtml);
    } else {
        bubble.textContent = contentHtml;
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatBox.appendChild(row);
    chatBox.scrollTop = chatBox.scrollHeight;

    return { row, bubble };
}

// ── TYPING INDICATOR ──────────────────────────────────────────────
function showTyping() {
    const row = document.createElement('div');
    row.classList.add('message-row', 'ai-row');
    row.id = 'typing-row';

    const avatar = document.createElement('div');
    avatar.classList.add('msg-avatar', 'ai-avatar');
    avatar.textContent = 'AI';

    const bubble = document.createElement('div');
    bubble.classList.add('typing-bubble');
    bubble.innerHTML = '<span></span><span></span><span></span>';

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatBox.appendChild(row);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById('typing-row');
    if (el) el.remove();
}

// ── PROGRESS BAR HELPERS ──────────────────────────────────────────
function startProgress() {
    progress.classList.add('loading');
    progress.style.width = '';
}

function stopProgress(success = true) {
    progress.classList.remove('loading');
    progress.style.width = '100%';
    progress.style.background = success
        ? 'linear-gradient(90deg, var(--violet), var(--accent))'
        : 'var(--red)';
    setTimeout(() => {
        progress.style.width = '0%';
        progress.style.background = 'linear-gradient(90deg, var(--violet), var(--accent))';
    }, 800);
}

// ── MAIN SEND FUNCTION ────────────────────────────────────────────
async function processQuestion() {
    const query = userInput.value.trim();
    if (!query || sendBtn.disabled) return;

    // UI: user message
    appendMessage('user', query);
    userInput.value = '';
    document.getElementById('char-count').textContent = '0 / 500';

    // UI: disable + progress
    sendBtn.disabled = true;
    userInput.disabled = true;
    startProgress();
    showTyping();

    // Increment query counter
    if (window._incrementQuery) window._incrementQuery();

    try {
        const res = await fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: query })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        hideTyping();
        stopProgress(true);
        appendMessage('ai', data.response);

    } catch (err) {
        hideTyping();
        stopProgress(false);

        const { bubble } = appendMessage('ai', '', true);
        bubble.classList.add('error-bubble');
        bubble.innerHTML = `
            <p style="color: var(--red); font-weight: 500; margin-bottom: 6px;">
                ⚠ Connection Failed
            </p>
            <p style="color: var(--text-2); font-size: 0.83rem; line-height: 1.6;">
                Python backend not detected. Make sure <code>App.py</code> is running on
                <code>http://127.0.0.1:5000</code>.
            </p>`;
    } finally {
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

// ── EVENT LISTENERS ───────────────────────────────────────────────
sendBtn.addEventListener('click', processQuestion);

userInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        processQuestion();
    }
});

// ── KEYBOARD SHORTCUT: FOCUS WITH '/' ────────────────────────────
document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== userInput) {
        e.preventDefault();
        userInput.focus();
    }
});

// ── AUTO-FOCUS ON LOAD ────────────────────────────────────────────
window.addEventListener('load', () => { userInput.focus(); });
