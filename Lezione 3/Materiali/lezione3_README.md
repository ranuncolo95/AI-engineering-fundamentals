# Lezione 3 — Conversazione & Memoria

📅 Martedì 26/05/2026 | ⏱ 5 ore | Monte ore: 15/30

---

## Obiettivi

Al termine di questa lezione saprai:

- Gestire la **conversation history** multi-turno
- Gestire la **context window** con truncation e sliding window
- Implementare lo **streaming** delle risposte
- Salvare la memoria su **file JSON** per renderla persistente tra sessioni

---

## File in questa cartella

| File | Descrizione |
|------|-------------|
| `Lezione3_Colab.ipynb` | Notebook con teoria, esempi e esercizi |
| `Lezione3_TUONOME.ipynb` | ← Il tuo notebook completato (da caricare) |

---

## Come seguire la lezione

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/marcouras/AI-engineering-fundamentals/blob/main/lezione3/Lezione3_Colab.ipynb)

1. Apri il notebook su Colab
2. `File → Salva una copia in Drive`
3. Esegui le celle dall'alto verso il basso

---

## Esercizi

| # | Difficoltà | Descrizione |
|---|-----------|-------------|
| 1 | ★☆☆ | Chatbot multi-turno con system prompt WiData |
| 2 | ★★☆ | Sliding window (mantieni ultimi 4 turni) |
| 3 | ★★☆ | Streaming con conteggio token |
| 4 | ★★★ | **Deliverable** — Chatbot CLI completo con memoria persistente |

---

## 📬 Compito a casa

Entro la sera della lezione:

```bash
cp ~/Downloads/Lezione3_TUONOME.ipynb lezione3/
git add lezione3/
git commit -m "Lezione 3 completata"
git push
```

---

## Deliverable

`chatbot_cli.py` con:
- History multi-turno
- Sliding window (max 10 messaggi)
- Streaming attivo
- Memoria persistente su `chat_history.json`
- System prompt WiData
- Loop interattivo con `input()` e comando `esci`

---

## Riferimenti Huyen

- **Cap. 2** (parziale) — context window, token, tokenizzazione, KV cache

---

## Prossima lezione

📅 **Giovedì 28/05** — RAG — Conoscenza Personalizzata

**Leggi prima:** Huyen Cap. 6 — sezione RAG
