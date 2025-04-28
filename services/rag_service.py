from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class ChromaCompatibleEmbeddings:
    def __init__(self, embeddings_model):
        self.embeddings_model = embeddings_model

    def __call__(self, input):
        return self.embeddings_model.embed_documents(input)

    def embed_documents(self, texts):
        return self.embeddings_model.embed_documents(texts)

    def embed_query(self, text):
        return self.embeddings_model.embed_query(text)

def get_qa_chain():
    original_embeddings = OpenAIEmbeddings()
    compatible_embeddings = ChromaCompatibleEmbeddings(original_embeddings)

    db = Chroma(
        persist_directory="db",
        embedding_function=compatible_embeddings
    )

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-4")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
