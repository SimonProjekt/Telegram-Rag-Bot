import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from services.rag_service import ChromaCompatibleEmbeddings

def create_database():
    file_path = os.path.join("data", "kallkritik.md")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filen saknas: {file_path}")

    print(f"🔄 Läser in: {file_path}")
    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documents = text_splitter.split_documents(documents)
    print(f"Antal dokument som laddats in: {len(documents)}")

    # Använd wrappern från rag_service
    original_embeddings = OpenAIEmbeddings()
    embeddings = ChromaCompatibleEmbeddings(original_embeddings)

    db = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory="db"
    )
    db.persist()
    print("✅ Databas skapad och sparad i ./db")

if __name__ == "__main__":
    load_dotenv()
    if not os.path.exists("db") or not os.listdir("db"):
        print("🛠️ Ingen db hittades, bygger om...")
        create_database()
    else:
        print("✅ db/ redan finns, använder den.")
