# Lezione 6 — UI Web, Valutazione & Deploy 🏁

📅 Martedì 09/06/2026 | ⏱ 5 ore | Monte ore: 30/30

---

## Obiettivi

Al termine di questa lezione saprai:

- Costruire una **chat UI** con Streamlit
- Gestire il **session state** tra un rerun e l'altro
- Valutare le risposte con **AI-as-a-Judge**
- Implementare **guardrails** di input e output
- **Deployare** su Streamlit Cloud con URL pubblico

---

## File in questa cartella

| File | Descrizione |
|------|-------------|
| `Lezione6_Colab.ipynb` | Notebook con teoria, esempi e esercizi |
| `app_completa.py` | App Streamlit finale (copia nella tua repo per il deploy) |
| `requirements.txt` | Dipendenze per Streamlit Cloud |
| `Lezione6_TUONOME.ipynb` | ← Il tuo notebook completato |

---

## Come seguire la lezione

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/marcouras/AI-engineering-fundamentals/blob/main/lezione6/Lezione6_Colab.ipynb)

---

## Esercizi

| # | Difficoltà | Descrizione |
|---|-----------|-------------|
| 1 | ★☆☆ | Personalizza la UI (sidebar, contatore, tema) |
| 2 | ★★☆ | Dataset di 10 Q&A con AI-as-a-Judge |
| 3 | ★★☆ | Guardrail output con logging su file |
| 4 | ★★★ | **Deliverable FINALE** — Deploy su Streamlit Cloud |

---

## 📬 Consegna finale

```bash
git add lezione6/
git add progetto_finale/
git commit -m "Corso completato — chatbot online!"
git push
```

---

## Deliverable finale

- ✅ URL pubblico su Streamlit Cloud
- ✅ Repository GitHub con README professionale
- ✅ Chatbot funzionante con almeno RAG o tool
- ✅ Presentazione 5 min con posizionamento Crawl-Walk-Run

---

## Deploy su Streamlit Cloud

1. Vai su [share.streamlit.io](https://share.streamlit.io)
2. **New app** → seleziona la tua repo
3. Main file: `lezione6/app_completa.py`
4. **Advanced** → Secrets → aggiungi `ANTHROPIC_API_KEY`
5. Deploy → attendi 3-5 minuti

> ⚠️ La prima build è lenta (~5 min) perché scarica sentence-transformers (~800MB)

---

## Riferimenti Huyen

- **Cap. 3 + 4** — Evaluation Methodology, AI-as-a-Judge, guardrails
- **Cap. 10** — AI Engineering Architecture, deployment, feedback loop

---

## 🎓 Fine del corso

In 30 ore hai costruito un chatbot AI completo — dalla prima riga di codice al deploy pubblico.

**Il link GitHub va sul CV. Adesso.**
