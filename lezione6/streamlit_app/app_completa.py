
import streamlit as st
import anthropic
import os
from pypdf import PdfReader
import io

st.set_page_config(page_title="Chatbot WiData", page_icon="🤖", layout="wide")

# API Key robusta — funziona su Streamlit Cloud e in locale
api_key = None
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass
if not api_key:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("❌ API key non trovata. Configura ANTHROPIC_API_KEY nei Secrets.")
    st.info("Su Streamlit Cloud: Manage app → Settings → Secrets")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

SYSTEM = """
Sei l'assistente virtuale di WiData Srl, startup IoT e smart cities di Sassari.
Rispondi SOLO basandoti sui documenti forniti nel contesto.
Se non hai informazioni sufficienti, dì: 'Non ho questa informazione.'
Non inventare mai dati tecnici, prezzi o specifiche.
"""

def chunka_testo(testo, chunk_size=400, overlap=50):
    chunks, start = [], 0
    while start < len(testo):
        chunk = testo[start:start+chunk_size]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def indicizza_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    testo = " ".join(p.extract_text() or "" for p in reader.pages)
    return chunka_testo(testo)

def cerca_rag(domanda, chunks, n=3):
    if not chunks:
        return []
    parole = [p for p in domanda.lower().split() if len(p) > 2]
    scored = [(sum(1 for p in parole if p in c.lower()), c) for c in chunks]
    scored.sort(reverse=True)
    return [c for _, c in scored[:n] if _ > 0]

def guardrail_input(testo):
    if len(testo) > 2000:
        return None, "Messaggio troppo lungo (max 2000 caratteri)"
    pattern_vietati = ["ignore previous instructions", "ignora le istruzioni"]
    if any(p in testo.lower() for p in pattern_vietati):
        return None, "Input non consentito"
    return testo, None

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "token_totali" not in st.session_state:
    st.session_state.token_totali = 0

with st.sidebar:
    st.title("⚙️ Impostazioni")
    nome_chatbot = st.text_input("Nome chatbot", "Chatbot WiData")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    n_chunks = st.slider("Chunk RAG", 1, 5, 3)
    st.divider()
    uploaded = st.file_uploader("📄 Carica PDF", type="pdf")
    if uploaded:
        with st.spinner("Indicizzando..."):
            st.session_state.chunks = indicizza_pdf(uploaded.read())
            st.success(f"✅ {len(st.session_state.chunks)} chunk indicizzati")
    st.divider()
    costo = st.session_state.token_totali / 1_000_000 * 1.0
    st.metric("Messaggi", len(st.session_state.messages))
    st.metric("Token usati", st.session_state.token_totali)
    st.metric("Costo stimato", f"${costo:.5f}")
    st.divider()
    if st.button("🗑️ Nuova chat"):
        st.session_state.messages = []
        st.session_state.token_totali = 0
        st.rerun()

st.title(f"🤖 {nome_chatbot}")
st.caption("Assistente virtuale per prodotti IoT e smart cities — WiData Srl")

if not st.session_state.chunks:
    st.info("💡 Carica un PDF dalla sidebar per attivare il RAG.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Scrivi un messaggio..."):
    testo_ok, errore = guardrail_input(prompt)
    if errore:
        st.error(errore)
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)

    chunks_trovati = cerca_rag(prompt, st.session_state.chunks, n_chunks)
    contesto = "\n\n---\n\n".join(chunks_trovati) if chunks_trovati else ""
    messaggio_rag = f"Contesto:\n\n{contesto}\n\n---\n\nDomanda: {prompt}" if contesto else prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    history_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
    history_api.append({"role": "user", "content": messaggio_rag})

    with st.chat_message("assistant"):
        risposta = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=700,
            temperature=temperature,
            system=SYSTEM,
            messages=history_api
        ) as stream:
            for text in stream.text_stream:
                risposta += text
                placeholder.markdown(risposta + "▌")
        placeholder.markdown(risposta)

        if chunks_trovati:
            with st.expander(f"📄 {len(chunks_trovati)} chunk RAG usati"):
                for i, c in enumerate(chunks_trovati):
                    st.caption(f"Chunk {i+1}: {c[:200]}...")

        st.feedback("thumbs")

    st.session_state.messages.append({"role": "assistant", "content": risposta})
    st.session_state.token_totali += len(risposta) // 4
