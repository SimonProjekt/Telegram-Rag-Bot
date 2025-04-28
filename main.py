from fastapi import FastAPI, Request
from models.query_request import QueryRequest
from services.telegram_service import send_telegram_message, send_typing_action
from services.rag_service import get_qa_chain
from utils.load_env import load_environment_variables
import uvicorn
from services.database_service import create_database
import os

# Starta om Chroma om db/ saknas
if not os.path.exists("db") or not os.listdir("db"):
    print("🛠️ Ingen db hittades, bygger om...")
    create_database()
else:
    print("✅ db/ hittades, fortsätter...")

# Ladda miljövariabler
load_environment_variables()

# Initiera FastAPI och QA-chain
app = FastAPI()
qa_chain = get_qa_chain()

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    result = qa_chain({"query": request.query})
    return {
        "answer": result["result"],
        "sources": [doc.page_content for doc in result["source_documents"]]
    }

@app.post("/webhook")
async def telegram_webhook(request: Request):
    body = await request.json()
    print("Telegram-meddelande mottaget:", body)

    try:
        chat_id = body["message"]["chat"]["id"]
        message_text = body["message"]["text"].strip().lower()

        print(f"Användaren skrev: {message_text}")

        send_typing_action(chat_id)

        if message_text == "/start":
            welcome_message = (
                "Hej! 👋 Jag är din utbildningsassistent.\n\n"
                "Ställ en fråga om källkritik, eller skriv /exercise för att få en övning!\n"
                "Använd /help om du vill veta vad jag kan göra."
            )
            send_telegram_message(chat_id, welcome_message)

        elif message_text == "/help":
            help_message = (
                "📚 Här är vad jag kan hjälpa dig med:\n"
                "- Ställ vanliga frågor om källkritik.\n"
                "- Skriv /exercise för att få en övningsuppgift.\n"
                "- Skriv /start för att se detta meddelande igen.\n"
                "\n"
                "Bara fråga på! 🚀"
            )
            send_telegram_message(chat_id, help_message)

        elif message_text == "/exercise":
            exercise_prompt = (
                "Skapa en enkel övningsuppgift baserad på utbildningsmaterialet om källkritik. "
                "Formulera en liten frågeställning eller en praktisk uppgift användaren kan göra."
            )
            exercise_response = qa_chain.invoke({"query": exercise_prompt})
            exercise = exercise_response["result"]

            send_telegram_message(chat_id, f"📝 Övning:\n\n{exercise}")

        else:
            # Vanlig fråga till RAG
            response = qa_chain.invoke({"query": message_text})
            answer = response["result"]

            print(f"Svar från RAG: {answer}")

            send_telegram_message(chat_id, answer)

        return {"status": "Message processed"}

    except Exception as e:
        print("Fel vid hantering av Telegram-meddelande:", str(e))
        return {"status": "error", "message": str(e)}

# Kör lokalt
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
