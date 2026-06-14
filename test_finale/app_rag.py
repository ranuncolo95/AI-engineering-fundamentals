
import streamlit as st
import anthropic, os, chromadb
from pypdf import PdfReader
from dotenv import load_dotenv, find_dotenv
import io

load_dotenv(find_dotenv(usecwd=True))

client = anthropic.Anthropic()
st.set_page_config(page_title="Chatbot RAG WiData", page_icon="🤖")

SYSTEM = """
Sei l'assistente di WiData Srl.
Rispondi SOLO basandoti sui documenti forniti nel contesto.
Se la risposta non è nei documenti, dì chiaramente che non hai questa informazione.
"""

# @st.cache_resource evita di reinizializzare ChromaDB ad ogni rerun
@st.cache_resource
def get_chroma_client():
    return chromadb.Client()

def chunka(testo, size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(testo):
        chunk = testo[start:start+size]
        if chunk.strip():
            chunks.append(chunk)
        start += size - overlap
    return chunks

def indicizza_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    testo = " ".join(p.extract_text() or "" for p in reader.pages)
    chunks = chunka(testo)
    chroma = get_chroma_client()
    try: chroma.delete_collection("rag_collection")
    except: pass
    coll = chroma.create_collection("rag_collection")
    coll.add(documents=chunks, ids=[str(i) for i in range(len(chunks))])
    return coll, len(chunks)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "collection" not in st.session_state:
    st.session_state.collection = None

# Sidebar
with st.sidebar:
    st.title("📄 Documento")
    uploaded = st.file_uploader("Carica PDF", type="pdf")
    if uploaded:
        with st.spinner("Indicizzando..."):
            coll, n = indicizza_pdf(uploaded.read())
            st.session_state.collection = coll
            st.success(f"✅ {n} chunk indicizzati")
    st.divider()
    if st.button("🗑️ Nuova chat"):
        st.session_state.messages = []
        st.rerun()

# Main
st.title("🤖 Chatbot RAG WiData")

if st.session_state.collection is None:
    st.info("Carica un PDF dalla sidebar per iniziare.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Scrivi un messaggio..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG
    chunks_trovati = []
    if st.session_state.collection:
        risultati = st.session_state.collection.query(
            query_texts=[prompt],
            n_results=min(3, st.session_state.collection.count())
        )
        chunks_trovati = risultati["documents"][0]

    contesto = "\n\n---\n\n".join(chunks_trovati) if chunks_trovati else ""
    messaggio_rag = f"Contesto:\n\n{contesto}\n\n---\n\nDomanda: {prompt}" if contesto else prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    history_rag = st.session_state.messages[:-1] + [{"role": "user", "content": messaggio_rag}]

    with st.chat_message("assistant"):
        risposta = ""
        placeholder = st.empty()
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=SYSTEM,
            messages=history_rag
        ) as stream:
            for text in stream.text_stream:
                risposta += text
                placeholder.markdown(risposta + "▌")
        placeholder.markdown(risposta)

        if chunks_trovati:
            with st.expander(f"📄 {len(chunks_trovati)} chunk RAG usati"):
                for i, c in enumerate(chunks_trovati):
                    st.caption(f"Chunk {i+1}: {c[:200]}...")

    st.session_state.messages.append({"role": "assistant", "content": risposta})
