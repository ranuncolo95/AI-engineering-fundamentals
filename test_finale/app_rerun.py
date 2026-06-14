
import streamlit as st
import anthropic, os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

client = anthropic.Anthropic()
st.set_page_config(page_title="Demo Rerun", page_icon="🔄")

# Contatore di rerun — dimostra che Streamlit riesegue tutto
if "rerun_count" not in st.session_state:
    st.session_state.rerun_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# Incrementiamo il contatore ad OGNI esecuzione dello script (cioè ad ogni rerun)
st.session_state.rerun_count += 1

# Sidebar con informazioni di debug
with st.sidebar:
    st.title("🔍 Debug")
    st.metric("Numero di rerun", st.session_state.rerun_count)
    st.metric("Messaggi in storia", len(st.session_state.messages))
    st.divider()
    if st.button("🗑️ Reset storia"):
        st.session_state.messages = []
        st.rerun()

st.title("Demo Rerun — Streamlit")
st.info("Ogni volta che invii un messaggio, Streamlit riesegue"
        " TUTTO lo script. Il session state mantiene i dati tra i rerun.")

# Chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Scrivi per vedere il rerun..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        risposta = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=st.session_state.messages
        ) as stream:
            for text in stream.text_stream:
                risposta += text
                placeholder.markdown(risposta + "▌")
        placeholder.markdown(risposta)

    st.session_state.messages.append({"role": "assistant", "content": risposta})
