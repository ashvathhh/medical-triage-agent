import streamlit as st
import pdfplumber
import io

st.set_page_config(
    page_title="Medical Triage Agent",
    page_icon="assets/icon.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Page background ── */
.stApp {
    background: #0a0f1e;
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1424;
    border-right: 1px solid #1e2d4a;
}

[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

.sidebar-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3b82f6 !important;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d4a;
}

.case-card {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: border-color 0.2s;
}

.case-card:hover {
    border-color: #3b82f6;
}

.case-card .case-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.urgency-HIGH   { color: #ef4444 !important; }
.urgency-MEDIUM { color: #f59e0b !important; }
.urgency-LOW    { color: #22c55e !important; }

.case-card .case-text {
    font-size: 13px;
    color: #64748b !important;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ── Header ── */
.app-header {
    padding: 32px 0 24px 0;
    margin-bottom: 8px;
}

.app-header h1 {
    font-size: 26px;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}

.app-header p {
    font-size: 14px;
    color: #475569;
    margin: 0;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.user-bubble {
    background: #1e3a5f;
    border: 1px solid #2563eb33;
    border-radius: 12px 12px 2px 12px;
    padding: 14px 18px;
    margin: 16px 0 4px auto;
    max-width: 80%;
    font-size: 14px;
    color: #e2e8f0;
    line-height: 1.6;
}

.assistant-bubble {
    background: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 2px 12px 12px 12px;
    padding: 18px 20px;
    margin: 4px 0 16px 0;
    max-width: 88%;
    font-size: 14px;
    color: #cbd5e1;
    line-height: 1.7;
}

/* ── Reasoning expander ── */
.reasoning-header {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3b82f6;
    margin: 12px 0 8px 0;
    cursor: pointer;
}

.reasoning-step {
    background: #0d1424;
    border-left: 2px solid #3b82f6;
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
}

.reasoning-step .tool-name {
    color: #3b82f6;
    font-weight: 500;
    margin-bottom: 4px;
}

.reasoning-step .tool-input {
    color: #94a3b8;
    margin-bottom: 4px;
}

.reasoning-step .tool-output {
    color: #64748b;
    font-size: 11px;
}

/* ── Urgency badge ── */
.urgency-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 10px;
}

.badge-HIGH   { background: #450a0a; color: #ef4444; border: 1px solid #ef444433; }
.badge-MEDIUM { background: #431407; color: #f59e0b; border: 1px solid #f59e0b33; }
.badge-LOW    { background: #052e16; color: #22c55e; border: 1px solid #22c55e33; }

/* ── PDF upload ── */
[data-testid="stFileUploader"] {
    background: #0d1424;
    border: 1px dashed #1e2d4a;
    border-radius: 10px;
    padding: 8px;
}

[data-testid="stFileUploader"] label {
    color: #475569 !important;
    font-size: 13px;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #111827 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 12px !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0d1424 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
}

[data-testid="stExpander"] summary {
    color: #475569 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* ── Divider ── */
hr {
    border-color: #1e2d4a !important;
}

/* ── Success/info alerts ── */
[data-testid="stAlert"] {
    background: #0d1424 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #64748b !important;
    font-size: 13px !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #3b82f6 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #1e2d4a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">Patient History</div>', unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        for i, case in enumerate(reversed(st.session_state.history)):
            urgency = case.get("urgency", "LOW")
            st.markdown(f"""
            <div class="case-card">
                <div class="case-label urgency-{urgency}">{urgency} urgency &mdash; Case {len(st.session_state.history) - i}</div>
                <div class="case-text">{case['input']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:13px; color:#334155;">No cases yet. Submit a patient case to begin.</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Upload Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload patient PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            pdf_text = "".join(page.extract_text() or "" for page in pdf.pages)
        st.session_state.pdf_context = pdf_text
        st.success(f"Document loaded: {len(pdf_text)} characters extracted.")


# ── Header ───────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1><span class="status-dot"></span>Medical Triage Agent</h1>
    <p>Agentic AI that researches, reasons, and triages patient cases autonomously</p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ── Agent init ───────────────────────────────────────────
if "agent" not in st.session_state:
    from agent.agent import create_medical_agent
    st.session_state.agent = create_medical_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Chat history ─────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        urgency = msg.get("urgency", "")
        badge = f'<span class="urgency-badge badge-{urgency}">{urgency} urgency</span>' if urgency else ""
        st.markdown(f'<div class="assistant-bubble">{msg["content"]}{badge}</div>', unsafe_allow_html=True)

        if msg.get("reasoning"):
            with st.expander("View reasoning steps"):
                for step in msg["reasoning"]:
                    st.markdown(f"""
                    <div class="reasoning-step">
                        <div class="tool-name">Tool: {step['tool']}</div>
                        <div class="tool-input">Input: {step['input']}</div>
                        <div class="tool-output">Result: {step['output'][:200]}...</div>
                    </div>
                    """, unsafe_allow_html=True)


# ── Chat input ───────────────────────────────────────────
if prompt := st.chat_input("Describe a patient case..."):
    full_prompt = prompt
    if "pdf_context" in st.session_state:
        full_prompt = f"Patient document:\n{st.session_state.pdf_context}\n\nQuestion: {prompt}"

    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Reasoning..."):
        response = st.session_state.agent.invoke(
            {"messages": [{"role": "user", "content": full_prompt}]}
        )

        output = response["messages"][-1].content

        # Strip emojis from output
        import re
        output = re.sub(r'[^\x00-\x7F\u00C0-\u024F\u1E00-\u1EFF]+', '', output).strip()

        reasoning_steps = []
        for m in response["messages"]:
            if hasattr(m, "tool_calls") and m.tool_calls:
                for tc in m.tool_calls:
                    reasoning_steps.append({
                        "tool": tc["name"],
                        "input": str(tc["args"]),
                        "output": ""
                    })
            if hasattr(m, "name") and m.name:
                if reasoning_steps:
                    reasoning_steps[-1]["output"] = m.content[:300]

        output_upper = output.upper()
        urgency = "HIGH" if "HIGH" in output_upper else "MEDIUM" if "MEDIUM" in output_upper else "LOW"
        badge = f'<span class="urgency-badge badge-{urgency}">{urgency} urgency</span>'

        st.markdown(f'<div class="assistant-bubble">{output}{badge}</div>', unsafe_allow_html=True)

        if reasoning_steps:
            with st.expander("View reasoning steps"):
                for step in reasoning_steps:
                    st.markdown(f"""
                    <div class="reasoning-step">
                        <div class="tool-name">Tool: {step['tool']}</div>
                        <div class="tool-input">Input: {step['input']}</div>
                        <div class="tool-output">Result: {step['output'][:200]}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": output,
            "urgency": urgency,
            "reasoning": reasoning_steps
        })

        st.session_state.history.append({
            "input": prompt,
            "urgency": urgency
        })

        st.rerun()