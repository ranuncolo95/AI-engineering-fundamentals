
import io
import streamlit as st
import anthropic
import chromadb

from pypdf import PdfReader
from dotenv import load_dotenv, find_dotenv
from chromadb.utils import embedding_functions

load_dotenv(find_dotenv(usecwd=True))

client = anthropic.Anthropic()

st.set_page_config(
    page_title="Chatbot RAG WiData",
    page_icon="🤖",
    layout="wide"
)

SYSTEM = """
Sei l'assistente di WiData Srl.

Rispondi esclusivamente utilizzando le informazioni presenti
nel contesto fornito.

Se la risposta non è contenuta nei documenti, dichiara
esplicitamente che non possiedi tale informazione.
"""

# --------------------------------------------------
# ChromaDB
# --------------------------------------------------

@st.cache_resource
def get_chroma_client():
    return chromadb.Client()

@st.cache_resource
def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

# --------------------------------------------------
# Chunking
# --------------------------------------------------

def chunka(testo, size=400, overlap=50):
    chunks = []

    start = 0

    while start < len(testo):
        chunk = testo[start:start + size]

        if chunk.strip():
            chunks.append(chunk)

        start += size - overlap

    return chunks

# --------------------------------------------------
# PDF → Chroma
# --------------------------------------------------

def indicizza_pdf(file_bytes):

    reader = PdfReader(io.BytesIO(file_bytes))

    testo = " ".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    chunks = chunka(testo)

    chroma = get_chroma_client()

    try:
        chroma.delete_collection("rag_collection")
    except Exception:
        pass

    collection = chroma.create_collection(
        name="rag_collection",
        embedding_function=get_embedding_function()
    )

    collection.add(
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )

    return collection, len(chunks)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "collection" not in st.session_state:
    st.session_state.collection = None

if "token_totali" not in st.session_state:
    st.session_state.token_totali = 0

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("⚙️ Impostazioni")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7
    )

    max_tokens = st.slider(
        "Max tokens",
        min_value=100,
        max_value=1000,
        value=500
    )

    st.divider()

    uploaded = st.file_uploader(
        "📄 Carica PDF",
        type="pdf"
    )

    if uploaded:

        with st.spinner("Indicizzazione PDF..."):

            collection, n_chunks = indicizza_pdf(
                uploaded.read()
            )

            st.session_state.collection = collection

        st.success(
            f"PDF caricato: {uploaded.name}"
        )

        st.info(
            f"Chunk indicizzati: {n_chunks}"
        )

    st.divider()

    costo = (
        st.session_state.token_totali
        / 1_000_000
        * 1.0
    )

    st.metric(
        "Token usati",
        st.session_state.token_totali
    )

    st.metric(
        "Costo stimato",
        f"${costo:.5f}"
    )

    st.divider()

    if st.button("🗑️ Nuova chat"):

        st.session_state.messages = []
        st.session_state.collection = None
        st.session_state.token_totali = 0

        st.rerun()

# --------------------------------------------------
# Main
# --------------------------------------------------

st.title("🤖 Chatbot RAG WiData")

if st.session_state.collection is None:
    st.info(
        "Carica un PDF dalla sidebar per iniziare."
    )

# Storico chat

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# Input utente
# --------------------------------------------------

if prompt := st.chat_input("Scrivi un messaggio..."):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # ----------------------------------------------
    # Retrieval
    # ----------------------------------------------

    chunks_trovati = []

    if st.session_state.collection:

        n_results = min(
            3,
            st.session_state.collection.count()
        )

        if n_results > 0:

            risultati = (
                st.session_state.collection.query(
                    query_texts=[prompt],
                    n_results=n_results
                )
            )

            chunks_trovati = risultati["documents"][0]

    # ----------------------------------------------
    # Context building
    # ----------------------------------------------

    if chunks_trovati:

        contesto = "\n\n---\n\n".join(
            chunks_trovati
        )

        messaggio_rag = f"""
Contesto:

{contesto}

---

Domanda:

{prompt}
"""

    else:

        messaggio_rag = prompt

    history_rag = (
        st.session_state.messages[:-1]
        +
        [{
            "role": "user",
            "content": messaggio_rag
        }]
    )

    # ----------------------------------------------
    # Claude
    # ----------------------------------------------

    with st.chat_message("assistant"):

        risposta = ""

        placeholder = st.empty()

        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            system=SYSTEM,
            messages=history_rag,
            max_tokens=max_tokens,
            temperature=temperature
        ) as stream:

            for text in stream.text_stream:

                risposta += text

                placeholder.markdown(
                    risposta + "▌"
                )

        placeholder.markdown(risposta)

        if chunks_trovati:

            with st.expander(
                f"📄 Chunk RAG utilizzati ({len(chunks_trovati)})"
            ):

                for i, chunk in enumerate(
                    chunks_trovati,
                    start=1
                ):

                    st.markdown(
                        f"**Chunk {i}**"
                    )

                    st.caption(
                        chunk[:500]
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": risposta
        }
    )

    # stima semplice token

    st.session_state.token_totali += (
        len(risposta) // 4
    )
