import streamlit as st
from agent.agent import create_medical_agent

st.set_page_config(page_title="Medical Triage Agent", page_icon="🏥")
st.title("🏥 Medical Triage Agent")
st.caption("An agentic AI that researches, reasons, and triages patient cases autonomously")

if "agent" not in st.session_state:
    st.session_state.agent = create_medical_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Describe a patient case..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning..."):
            response = st.session_state.agent.invoke({"input": prompt})
            output = response["output"]
            st.write(output)
            st.session_state.messages.append({"role": "assistant", "content": output})