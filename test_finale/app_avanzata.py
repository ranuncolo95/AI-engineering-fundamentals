
import streamlit as st
import anthropic, os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

st.set_page_config(page_title="Chatbot WiData Pro", page_icon="🤖", layout="wide")

# API key robusta — funziona su Streamlit Cloud (Secrets) e in locale (.env)
api_key = None
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass
if not api_key:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("❌ API key non trovata. Configura ANTHROPIC_API_KEY nei Secrets o nel file .env.")
    st.info("Su Streamlit Cloud: Manage app → Settings → Secrets")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

SYSTEM = """
Sei l'assistente virtuale di WiData Srl, startup IoT e smart cities di Sassari.
Rispondi in modo chiaro, professionale e cordiale.
"""

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "token_totali" not in st.session_state:
    st.session_state.token_totali = 0

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Impostazioni")

    # Slider per la temperature
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    # Slider per max_tokens
    max_tokens = st.slider("Max tokens", 100, 1000, 500)

    st.divider()

    # File uploader per PDF (in questo esercizio lo mostriamo soltanto)
    uploaded = st.file_uploader("📄 Carica PDF", type="pdf")
    if uploaded:
        st.success(f"Caricato: {uploaded.name}")

    st.divider()

    # Metriche: messaggi, token totali e costo stimato (Haiku: $1 / milione di token)
    costo = st.session_state.token_totali / 1_000_000 * 1.0
    st.metric("Messaggi", len(st.session_state.messages))
    st.metric("Token usati", st.session_state.token_totali)
    st.metric("Costo stimato", f"${costo:.5f}")

    st.divider()
    if st.button("🗑️ Nuova chat"):
        st.session_state.messages = []
        st.session_state.token_totali = 0
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────
st.title("🤖 Chatbot WiData Pro")
st.caption("Assistente virtuale per prodotti IoT e smart cities — WiData Srl")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Scrivi un messaggio..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        risposta = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            temperature=temperature,
            system=SYSTEM,
            messages=st.session_state.messages
        ) as stream:
            for text in stream.text_stream:
                risposta += text
                placeholder.markdown(risposta + "▌")
        placeholder.markdown(risposta)

        # Feedback thumbs up/down sotto la risposta
        st.feedback("thumbs")

    st.session_state.messages.append({"role": "assistant", "content": risposta})
    # Stima dei token usati dalla risposta (~4 caratteri per token)
    st.session_state.token_totali += len(risposta) // 4
