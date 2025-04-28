# Telegram-Rag-Bot 📚🤖

En FastAPI-baserad AI-chatbot som använder Retrieval-Augmented Generation (RAG) för att svara på frågor baserat på utbildningsmaterial om källkritik. Botten är kopplad till Telegram och kan även skapa övningar på begäran.

---

## ✨ Funktioner
- Svara på frågor baserat på inläst utbildningsmaterial.
- Skapa övningsuppgifter relaterade till materialet via kommandot `/exercise`.
- Hantera vanliga kommandon som `/start` och `/help`.
- Integration mot Telegram via Webhooks.
- Byggd med RAG-teknik: OpenAI GPT-4 + Chroma Vector Database.
- Strukturerad och modulär kodbas enligt moderna backend-principer.

---

## 🛠 Teknikstack
- Python 3.11
- FastAPI
- LangChain
- Chroma (vektor-databas)
- OpenAI GPT-4
- Telegram Bot API
- Docker (planerat för containerisering)
- Kubernetes (planerad deployment)

---

## 🚀 Snabbstart

1. Klona repot:
   ```bash
   git clone https://github.com/dittanamn/rag-telegram-bot.git
   cd rag-telegram-bot

