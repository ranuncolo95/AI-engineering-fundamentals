
import streamlit as st
import anthropic
import os

# Configurazione pagina
st.set_page_config(
    page_title="Chatbot WiData",
    page_icon="🤖",
    layout="wide"
)

# API key (da Streamlit Secrets in produzione)
if "ANTHROPIC_API_KEY" in st.secrets:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic()

SYSTEM = """
Sei l'assistente virtuale di WiData Srl, startup IoT e smart cities di Sassari.
Rispondi in modo professionale e conciso.
Se non hai informazioni sufficienti, dillo chiaramente.
"""

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Impostazioni")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max token risposta", 100, 1000, 500, 50)
    st.divider()
    if st.button("🗑️ Nuova conversazione"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("WiData Srl — AI Engineering Fundamentals")
    st.caption("ITS Novitas 4.0 | 2026")

# ── Titolo ────────────────────────────────────────────────────────
st.title("🤖 Chatbot WiData")
st.caption("Assistente virtuale per prodotti IoT e smart cities")

# ── Session state (memoria tra rerun) ────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Mostra history ────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input utente ─────────────────────────────────────────────────
if prompt := st.chat_input("Scrivi un messaggio..."):

    # Guardrail input
    if len(prompt) > 2000:
        st.error("Messaggio troppo lungo (max 2000 caratteri)")
        st.stop()

    # Mostra messaggio utente
    with st.chat_message("user"):
        st.markdown(prompt)

    # Aggiungi alla history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Genera risposta con streaming
    with st.chat_message("assistant"):
        with st.spinner("Elaboro..."):
            risposta_completa = ""
            placeholder = st.empty()

            with client.messages.stream(
                model="claude-haiku-4-5-20251001",
                max_tokens=max_tokens,
                temperature=temperature,
                system=SYSTEM,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ) as stream:
                for text in stream.text_stream:
                    risposta_completa += text
                    placeholder.markdown(risposta_completa + "▌")

            placeholder.markdown(risposta_completa)

    # Aggiungi risposta alla history
    st.session_state.messages.append({"role": "assistant", "content": risposta_completa})
