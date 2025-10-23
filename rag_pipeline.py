from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.schema import HumanMessage, SystemMessage
from config import OPENAI_API_KEY, OPENAI_MODEL
import os

# LangChain reads API key from OPENAI_API_KEY env var. We already loaded it via config.py

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

def build_rag(documents):
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

def get_agent_response(vector_store, prompt):
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
    docs = vector_store.similarity_search(prompt, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    
    messages = [
        SystemMessage(content="Use the context to answer."),
        HumanMessage(content=f"{prompt}\n\nContext:\n{context}")
    ]
    
    response = llm.generate([messages])
    return response.generations[0][0].text