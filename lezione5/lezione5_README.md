# Lezione 5 — Tools, Function Calling & MCP

📅 Giovedì 04/06/2026 | ⏱ 5 ore | Monte ore: 25/30

---

## Obiettivi

Al termine di questa lezione saprai:

- Capire il **loop agente**: Percezione → Ragionamento → Azione → Osservazione
- Definire **tool in JSON** e integrarli nell'API Anthropic
- Implementare il **tool loop** con `while stop_reason == "tool_use"`
- Costruire 3 tool reali: **calcolatrice**, **meteo**, **Wikipedia**
- Capire **MCP** (Model Context Protocol) e il suo ecosistema

---

## File in questa cartella

| File | Descrizione |
|------|-------------|
| `Lezione5_Colab.ipynb` | Notebook con teoria, esempi e esercizi |
| `Lezione5_TUONOME.ipynb` | ← Il tuo notebook completato (da caricare) |

---

## Come seguire la lezione

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/marcouras/AI-engineering-fundamentals/blob/main/lezione5/Lezione5_Colab.ipynb)

---

## Esercizi

| # | Difficoltà | Descrizione |
|---|-----------|-------------|
| 1 | ★☆☆ | Tool `converti_unita` (km/miglia, celsius/fahrenheit) |
| 2 | ★★☆ | Multi-step con tool concatenati |
| 3 | ★★☆ | Tool meteo con fallback per città non in lista |
| 4 | ★★★ | **Deliverable** — Chatbot completo: RAG + 3 tool + MCP |

---

## 📬 Compito a casa

Entro la sera della lezione:

```bash
cp ~/Downloads/Lezione5_TUONOME.ipynb lezione5/
git add lezione5/
git commit -m "Lezione 5 completata"
git push
```

---

## Deliverable

Chatbot con:
- Tool calcolatrice, meteo (open-meteo.com), Wikipedia
- MCP server filesystem connesso
- RAG dal documento WiData (Lezione 4)
- Conversation history + streaming
- System prompt WiData con indicazioni sui tool

---

## Risorse utili

- [open-meteo.com](https://open-meteo.com) — API meteo gratuita, nessuna chiave
- [modelcontextprotocol.io](https://modelcontextprotocol.io) — Server MCP ufficiali
- [docs.anthropic.com/tool-use](https://docs.anthropic.com/tool-use) — Documentazione tool use

---

## Riferimenti Huyen

- **Cap. 6** — sezione Agents: loop agente, tool use, minimal footprint

---

## Prossima lezione

📅 **Martedì 09/06** — UI Web, Valutazione & Deploy 🚀

**È l'ultima lezione — tutto va online!**

**Leggi prima:** Huyen Cap. 3 + 4 (Evaluation) e Cap. 10 (Architecture)
