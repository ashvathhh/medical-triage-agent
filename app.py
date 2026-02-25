import streamlit as st
import pdfplumber
import io
import re

st.set_page_config(
    page_title="TriageAI — Clinical Decision Support",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; font-size: 16px; }
.stApp { background: #f0f4f8 !important; color: #1a2332; }
footer, #MainMenu, header { display: none !important; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; }

/* ── Topbar ── */
.topbar {
    background: #fff; border-bottom: 1px solid #e2e8f0;
    padding: 0 32px; height: 60px;
    display: flex; align-items: center; justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.topbar-left { display: flex; align-items: center; gap: 12px; }
.logo-box {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #0f62fe, #0043ce);
    border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-size: 16px; font-weight: 700; color: white;
    box-shadow: 0 2px 8px rgba(15,98,254,0.35);
}
.brand { font-size: 18px; font-weight: 600; color: #1a2332; letter-spacing: -0.01em; }
.pipe { color: #cbd5e1; font-weight: 300; font-size: 20px; }
.module-name { font-size: 15px; color: #64748b; }
.topbar-right { display: flex; align-items: center; gap: 16px; }
.sys-status {
    display: flex; align-items: center; gap: 7px;
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 20px; padding: 5px 14px;
    font-size: 13px; font-weight: 500; color: #15803d;
}
.live-dot { width: 7px; height: 7px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
.avatar {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #0f62fe, #7c3aed);
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 13px; font-weight: 600; color: white;
    box-shadow: 0 2px 6px rgba(15,98,254,0.3);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e2e8f0 !important; }
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
.sb-header { background: linear-gradient(135deg, #0f62fe 0%, #0043ce 100%); padding: 22px 18px 18px; }
.sb-header-title { font-size: 16px; font-weight: 600; color: white; margin-bottom: 3px; }
.sb-header-sub { font-size: 13px; color: rgba(255,255,255,0.65); }
.sb-section { padding: 16px 16px 12px; border-bottom: 1px solid #f1f5f9; }
.sb-label { font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #94a3b8; margin-bottom: 12px; }

.stat-row { display: flex; gap: 8px; }
.stat-box {
    flex: 1; background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 14px 10px 12px; text-align: center;
    transition: transform 0.15s;
}
.stat-box:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.stat-num { font-size: 26px; font-weight: 600; color: #1a2332; line-height: 1; }
.stat-lbl { font-size: 12px; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.06em; }
.stat-high .stat-num { color: #dc2626; }
.stat-medium .stat-num { color: #d97706; }
.stat-low .stat-num { color: #16a34a; }

.case-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 13px 14px; margin-bottom: 8px; transition: all 0.15s;
}
.case-card:hover { background: #f1f5f9; border-color: #93c5fd; transform: translateX(2px); }
.case-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.case-num { font-size: 12px; font-weight: 600; color: #94a3b8; letter-spacing: 0.08em; text-transform: uppercase; }
.case-text { font-size: 13px; color: #475569; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.badge { display: inline-block; padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
.badge-HIGH   { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.badge-MEDIUM { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.badge-LOW    { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

/* ── File uploader ── */
[data-testid="stFileUploader"] { background: #f8fafc !important; border: 1.5px dashed #cbd5e1 !important; border-radius: 10px !important; }
[data-testid="stFileUploader"] section { background: transparent !important; border: none !important; padding: 14px !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploader"] label { color: #64748b !important; font-size: 14px !important; }
[data-testid="stFileUploader"] button { background: #0f62fe !important; color: white !important; border: none !important; border-radius: 6px !important; font-size: 13px !important; padding: 5px 16px !important; }

/* ── Main area ── */
.main-wrap { max-width: 900px; margin: 0 auto; padding: 32px 24px 32px; }
.section-heading {
    font-size: 13px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #64748b;
    display: flex; align-items: center; gap: 8px; margin-bottom: 24px;
}
.section-heading::before { content: ''; display: inline-block; width: 3px; height: 16px; background: #0f62fe; border-radius: 2px; }

/* ── Info cards ── */
.info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px; }
.info-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 32px 24px 28px; text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: all 0.2s;
}
.info-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(15,98,254,0.1); border-color: #93c5fd; }
.info-card-icon { width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin: 0 auto 18px; }
.icon-blue   { background: #eff6ff; border: 1px solid #bfdbfe; }
.icon-green  { background: #f0fdf4; border: 1px solid #bbf7d0; }
.icon-purple { background: #faf5ff; border: 1px solid #e9d5ff; }
.info-card-title { font-size: 16px; font-weight: 600; color: #1e293b; margin-bottom: 10px; }
.info-card-desc { font-size: 14px; color: #64748b; line-height: 1.6; }

.empty-hint {
    background: white; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 36px 32px; text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.empty-hint-title { font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 10px; }
.empty-hint-sub { font-size: 15px; color: #64748b; line-height: 1.7; max-width: 440px; margin: 0 auto; }

/* ── Messages ── */
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 16px; }
.msg-user-bubble {
    max-width: 70%; background: linear-gradient(135deg, #0f62fe, #0043ce);
    color: white; border-radius: 16px 16px 3px 16px;
    padding: 16px 20px; font-size: 15px; line-height: 1.65;
    box-shadow: 0 4px 12px rgba(15,98,254,0.25);
}
.msg-ai { display: flex; gap: 12px; margin-bottom: 8px; }
.msg-ai-avatar {
    width: 38px; height: 38px; flex-shrink: 0;
    background: linear-gradient(135deg, #0f62fe, #7c3aed);
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 13px; font-weight: 700; color: white;
    box-shadow: 0 2px 8px rgba(15,98,254,0.25);
}
.msg-ai-bubble {
    flex: 1; background: white; border: 1px solid #e2e8f0;
    border-radius: 3px 16px 16px 16px; padding: 20px 24px;
    font-size: 15px; line-height: 1.8; color: #334155;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.msg-meta { display: flex; align-items: center; gap: 10px; margin-top: 14px; padding-top: 12px; border-top: 1px solid #f1f5f9; }
.urgency-pill { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.pill-HIGH   { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.pill-MEDIUM { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.pill-LOW    { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.pill-dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-HIGH { background: #dc2626; }
.dot-MEDIUM { background: #d97706; }
.dot-LOW { background: #16a34a; }
.powered-by { font-size: 12px; color: #94a3b8; margin-left: auto; }

/* ── Reasoning ── */
[data-testid="stExpander"] { background: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 10px !important; margin-top: 10px !important; }
[data-testid="stExpander"] summary { font-size: 13px !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: #64748b !important; }
.r-step { padding: 10px 14px; border-left: 2px solid #0f62fe; margin-bottom: 10px; border-radius: 0 8px 8px 0; background: white; }
.r-tool { font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #0f62fe; font-weight: 500; }
.r-input { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #64748b; margin-top: 3px; }
.r-output { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #94a3b8; margin-top: 3px; }

/* ── Input card — top half ── */
.input-card-top {
    background: white;
    border: 1px solid #e2e8f0;
    border-bottom: none;
    border-radius: 16px 16px 0 0;
    padding: 28px 32px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.input-card-top p.title { font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 6px; }
.input-card-top p.sub { font-size: 15px; color: #94a3b8; line-height: 1.6; }

/* ── Input card — bottom half ── */
div[data-testid="stHorizontalBlock"] {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    padding: 12px 28px 24px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    margin-top: 0 !important;
    gap: 12px !important;
}

/* ── Text input — kill ALL default browser and Streamlit styling ── */
.stTextInput { margin-bottom: 0 !important; }
.stTextInput > div {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}
.stTextInput > div:focus-within {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
.stTextInput > div > div {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}
.stTextInput > div > div > input {
    background: #f8fafc !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: #1a2332 !important;
    caret-color: #1a2332 !important;
    box-shadow: none !important;
    outline: none !important;
    width: 100% !important;
    -webkit-appearance: none !important;
}
.stTextInput > div > div > input:focus,
.stTextInput > div > div > input:focus-visible,
.stTextInput > div > div > input:focus-within,
.stTextInput > div > div > input:active {
    border-color: #0f62fe !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(15,98,254,0.1) !important;
    outline: none !important;
    caret-color: #1a2332 !important;
}
.stTextInput label { display: none !important; }

/* ── Analyse button ── */
.stButton > button {
    background: linear-gradient(135deg, #0f62fe, #0043ce) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 12px 24px !important;
    font-size: 15px !important; font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(15,98,254,0.3) !important;
    transition: all 0.2s !important; width: 100% !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    height: 52px !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(15,98,254,0.4) !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f0f4f8; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Topbar ───────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="logo-box">T</div>
        <span class="brand">TriageAI</span>
        <span class="pipe">|</span>
        <span class="module-name">Clinical Decision Support</span>
    </div>
    <div class="topbar-right">
        <div class="sys-status"><div class="live-dot"></div>System Operational</div>
        <div class="avatar">AC</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    from agent.agent import create_medical_agent
    st.session_state.agent = create_medical_agent()


# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-header-title">Clinical Workspace</div>
        <div class="sb-header-sub">Ashvath Cheppalli · Physician Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    total  = len(st.session_state.history)
    high   = sum(1 for c in st.session_state.history if c.get("urgency") == "HIGH")
    medium = sum(1 for c in st.session_state.history if c.get("urgency") == "MEDIUM")
    low    = sum(1 for c in st.session_state.history if c.get("urgency") == "LOW")

    st.markdown(f"""
    <div class="sb-section">
        <div class="sb-label">Session Summary</div>
        <div class="stat-row">
            <div class="stat-box"><div class="stat-num">{total}</div><div class="stat-lbl">Total</div></div>
            <div class="stat-box stat-high"><div class="stat-num">{high}</div><div class="stat-lbl">High</div></div>
            <div class="stat-box stat-medium"><div class="stat-num">{medium}</div><div class="stat-lbl">Med</div></div>
            <div class="stat-box stat-low"><div class="stat-num">{low}</div><div class="stat-lbl">Low</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section"><div class="sb-label">Patient Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            pdf_text = "".join(page.extract_text() or "" for page in pdf.pages)
        st.session_state.pdf_context = pdf_text
        st.success(f"Loaded — {len(pdf_text)} chars extracted")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section"><div class="sb-label">Case History</div>', unsafe_allow_html=True)
    if st.session_state.history:
        for i, case in enumerate(reversed(st.session_state.history)):
            urgency = case.get("urgency", "LOW")
            num = len(st.session_state.history) - i
            st.markdown(f"""
            <div class="case-card">
                <div class="case-card-top">
                    <span class="case-num">Case #{num:03d}</span>
                    <span class="badge badge-{urgency}">{urgency}</span>
                </div>
                <div class="case-text">{case['input']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:14px;color:#94a3b8;padding:6px 0 10px;">No cases submitted yet.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Main ─────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Patient Case Analysis</div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="info-grid">
        <div class="info-card">
            <div class="info-card-icon icon-blue">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            </div>
            <div class="info-card-title">Urgency Assessment</div>
            <div class="info-card-desc">Instantly classifies cases as HIGH, MEDIUM, or LOW urgency based on presented symptoms</div>
        </div>
        <div class="info-card">
            <div class="info-card-icon icon-green">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            </div>
            <div class="info-card-title">PubMed Research</div>
            <div class="info-card-desc">Searches real-time medical literature from the NCBI PubMed database automatically</div>
        </div>
        <div class="info-card">
            <div class="info-card-icon icon-purple">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/></svg>
            </div>
            <div class="info-card-title">Drug Interactions</div>
            <div class="info-card-desc">Cross-references the FDA drug database for warnings and contraindications</div>
        </div>
    </div>
    <div class="empty-hint">
        <div class="empty-hint-title">Ready to analyse a patient case</div>
        <div class="empty-hint-sub">Describe the patient symptoms, age, current medications and relevant medical history in the input below.</div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-user"><div class="msg-user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        urgency = msg.get("urgency", "LOW")
        st.markdown(f"""
        <div class="msg-ai">
            <div class="msg-ai-avatar">AI</div>
            <div class="msg-ai-bubble">
                {msg["content"]}
                <div class="msg-meta">
                    <span class="urgency-pill pill-{urgency}"><span class="pill-dot dot-{urgency}"></span>{urgency} Urgency</span>
                    <span class="powered-by">Llama 3.3 · PubMed · OpenFDA</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if msg.get("reasoning"):
            with st.expander("View reasoning trace"):
                for step in msg["reasoning"]:
                    st.markdown(f"""
                    <div class="r-step">
                        <div class="r-tool">Tool: {step['tool']}</div>
                        <div class="r-input">Input: {step['input'][:120]}</div>
                        <div class="r-output">Result: {step['output'][:200]}</div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Input section ─────────────────────────────────────────
st.markdown("<div style='max-width:900px; margin: 0 auto; padding: 0 24px 40px;'>", unsafe_allow_html=True)

st.markdown("""
<div class="input-card-top">
    <p class="title">Describe your patient case</p>
    <p class="sub">Include the patient age, symptoms, current medications and any relevant medical history for the most accurate triage.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col1:
    prompt = st.text_input(
        "case_input",
        placeholder="e.g. 58 year old male, chest pain and shortness of breath, currently on metformin...",
        label_visibility="collapsed",
        key="case_input"
    )
with col2:
    submit = st.button("Analyse")

st.markdown("</div>", unsafe_allow_html=True)

if submit and prompt:
    full_prompt = prompt
    if "pdf_context" in st.session_state:
        full_prompt = f"Patient document:\n{st.session_state.pdf_context}\n\nQuestion: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Analysing case..."):
        response = st.session_state.agent.invoke(
            {"messages": [{"role": "user", "content": full_prompt}]}
        )
        output = response["messages"][-1].content
        output = re.sub(r'[^\x00-\x7F\u00C0-\u024F\u1E00-\u1EFF]+', '', output).strip()

        reasoning_steps = []
        for m in response["messages"]:
            if hasattr(m, "tool_calls") and m.tool_calls:
                for tc in m.tool_calls:
                    reasoning_steps.append({"tool": tc["name"], "input": str(tc["args"]), "output": ""})
            if hasattr(m, "name") and m.name:
                if reasoning_steps:
                    reasoning_steps[-1]["output"] = m.content[:300]

        output_upper = output.upper()
        urgency = "HIGH" if "HIGH" in output_upper else "MEDIUM" if "MEDIUM" in output_upper else "LOW"

        st.session_state.messages.append({
            "role": "assistant", "content": output,
            "urgency": urgency, "reasoning": reasoning_steps
        })
        st.session_state.history.append({"input": prompt, "urgency": urgency})
        st.rerun()