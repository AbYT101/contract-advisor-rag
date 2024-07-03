import os
import tempfile
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate, Chroma
from api.services import file_service
import requests
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) 

def create_retriever():
    content = file_service.get_file_content()
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    loader = TextLoader(file_path=temp_file_path)
    docs = loader.load()

    embeddings = OpenAIEmbeddings()

    # Using Chroma as the vector store
    db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever()

    # Clean up the temporary file
    os.remove(temp_file_path)
    
    return retriever
