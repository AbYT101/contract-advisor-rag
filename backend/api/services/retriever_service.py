from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Weaviate, Chroma
from langchain.chains import RetrievalQA
from api.services import file_service

def create_retriever():
    content = file_service.get_file_content()
    loader = TextLoader(content=content)
    docs = loader.load()

    embeddings = OpenAIEmbeddings()
    
    # Choose either Weaviate or Chroma
    db = Weaviate.from_documents(docs, embeddings)
    # db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever()
    return retriever