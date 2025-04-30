from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Wrapper för att göra OpenAIEmbeddings kompatibelt med Chroma
class ChromaCompatibleEmbeddings:
    def __init__(self, embeddings_model):
        self.embeddings_model = embeddings_model

    # Gör klassen "callable" så den fungerar som funktion
    def __call__(self, input):
        return self.embeddings_model.embed_documents(input)

    # Embedda dokument (listor av textstycken)
    def embed_documents(self, texts):
        return self.embeddings_model.embed_documents(texts)

    # Embedda en enskild fråga (query)
    def embed_query(self, text):
        return self.embeddings_model.embed_query(text)

# Funktion som bygger upp hela RAG-kedjan
def get_qa_chain():
    # Initiera OpenAI-embeddings
    original_embeddings = OpenAIEmbeddings()

    # Slå in embeddings i wrapper så den funkar med Chroma
    compatible_embeddings = ChromaCompatibleEmbeddings(original_embeddings)

    # Ladda vektor-databasen från den lokala "db/"-mappen
    db = Chroma(
        persist_directory="db",                     # Här sparas eller läses in indexet
        embedding_function=compatible_embeddings   # Embeddings används för att jämföra likhet
    )

    # Skapa en retriever som hämtar de 4 mest relevanta dokumenten
    retriever = db.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 4}
    )

    # Initiera språkmodellen (GPT-4) via LangChain
    llm = ChatOpenAI(model="gpt-4")

    # Bygg RAG-kedjan: kombinerar retriever + GPT
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # Returerar även vilka dokument som användes
    )

    # Returnerar hela kedjan – redo att användas för frågor
    return qa_chain

