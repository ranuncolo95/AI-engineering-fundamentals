"""
AI Engineering Fundamentals — Lezione 1
Prima chiamata all'API di Claude

ITS Novitas 4.0 | Docente: Marco Uras
"""

import anthropic
from dotenv import load_dotenv

# Carica la API key dal file .env
load_dotenv()

# Crea il client Anthropic
# Legge automaticamente ANTHROPIC_API_KEY dall'ambiente
client = anthropic.Anthropic()

# Invia un messaggio a Claude
message = client.messages.create(
    model="claude-haiku-4-5-20251001",   # modello veloce per esercizi
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Ciao! Presentati in 2 righe e dimmi cosa puoi fare per me."
        }
    ]
)

# Stampa la risposta
print("=" * 50)
print("RISPOSTA DI CLAUDE:")
print("=" * 50)
print(message.content[0].text)
print()
print(f"[Token usati: {message.usage.input_tokens} input, {message.usage.output_tokens} output]")
