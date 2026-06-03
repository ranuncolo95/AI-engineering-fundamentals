# Lezione 4 — RAG: Conoscenza Personalizzata

📅 Giovedì 28/05/2026 | ⏱ 5 ore | Monte ore: 20/30

---

## Obiettivi

Al termine di questa lezione saprai:

- Capire la **pipeline RAG** completa (Ingest → Retrieve → Augment → Generate)
- Indicizzare documenti PDF con **ChromaDB**
- Implementare la **ricerca semantica**
- Costruire il **prompt aumentato** con il contesto recuperato
- Gestire i principali **fallimenti del retrieval**

---

## File in questa cartella

| File | Descrizione |
|------|-------------|
| `Lezione4_Colab.ipynb` | Notebook con teoria, esempi e esercizi |
| `Lezione4_TUONOME.ipynb` | ← Il tuo notebook completato (da caricare) |

---

## Come seguire la lezione

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/marcouras/AI-engineering-fundamentals/blob/main/lezione4/Lezione4_Colab.ipynb)

1. Apri il notebook su Colab
2. `File → Salva una copia in Drive`
3. Esegui le celle dall'alto verso il basso

> ⚠️ **Prima esecuzione lenta**: ChromaDB scarica il modello Sentence Transformers (~90MB). Solo la prima volta!

---

## Esercizi

| # | Difficoltà | Descrizione |
|---|-----------|-------------|
| 1 | ★☆☆ | Indicizza un documento tuo in ChromaDB |
| 2 | ★★☆ | Sperimenta con chunk_size=200, 400, 800 |
| 3 | ★★☆ | RAG + conversation history integrati |
| 4 | ★★★ | **Deliverable** — Chatbot RAG WiData completo |

---

## 📬 Compito a casa

Entro la sera della lezione:

```bash
cp ~/Downloads/Lezione4_TUONOME.ipynb lezione4/
git add lezione4/
git commit -m "Lezione 4 completata"
git push
```

---

## Deliverable

Chatbot RAG con:
- PDF indicizzato in ChromaDB
- Ricerca semantica funzionante
- Prompt aumentato con contesto RAG
- Streaming + conversation history
- System prompt WiData con istruzione anti-hallucination

---

## Riferimenti Huyen

- **Cap. 6** — sezione RAG: pipeline, chunking, retrieval failures, reranking

---

## Prossima lezione

📅 **Giovedì 04/06** — Tools, Function Calling & MCP

**Leggi prima:** Huyen Cap. 6 — sezione Agents
