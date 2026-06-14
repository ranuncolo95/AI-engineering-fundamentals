
import streamlit as st
import anthropic
import os
from dotenv import load_dotenv, find_dotenv

# Carica la API key dal .env nella root del progetto
load_dotenv(find_dotenv(usecwd=True))

# Configurazione pagina
st.set_page_config(
    page_title="Chatbot WiData",
    page_icon="🤖",
    layout="centered"
)

client = anthropic.Anthropic()

SYSTEM = "Sei l'assistente di WiData Srl, startup IoT di Sassari."

# 1) Inizializziamo il session state per la history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Chatbot WiData")
st.caption("Assistente virtuale per prodotti IoT e smart cities")

# 2) Mostriamo i messaggi della history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3) Gestiamo l'input utente e generiamo la risposta (in streaming)
if prompt := st.chat_input("Scrivi un messaggio..."):
    # mostra e salva il messaggio utente
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # genera la risposta dell'assistente
    with st.chat_message("assistant"):
        risposta = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=SYSTEM,
            messages=st.session_state.messages,
        ) as stream:
            for text in stream.text_stream:
                risposta += text
                placeholder.markdown(risposta + "▌")
        placeholder.markdown(risposta)

    st.session_state.messages.append({"role": "assistant", "content": risposta})
