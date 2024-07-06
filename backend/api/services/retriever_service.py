import os
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())

DATA_DIR = 'data/texts'
KNOWLEDGE_FILE = 'knowledge.txt'

def create_retriever():
    try:
        knowledge_file_path = os.path.join(DATA_DIR, KNOWLEDGE_FILE)

        if not os.path.isfile(knowledge_file_path):
            raise FileNotFoundError(f"{knowledge_file_path} does not exist or is not a file.")

        logging.info(f"Attempting to load {knowledge_file_path}")

        # Load the text data from the file
        loader = TextLoader(file_path=knowledge_file_path, encoding='utf-8')
        documents = loader.load()

        # Extract text from each Document object and concatenate into a single string
        raw_text = " ".join([doc.page_content for doc in documents])

        # Ensure the raw_text is now a string
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected a string after concatenation, but got {type(raw_text)}")

        # Split the text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Adjust based on the token limit
            chunk_overlap=50
        )
        docs = text_splitter.split_text(raw_text)

        # Ensure the docs are a list of strings
        if not all(isinstance(doc, str) for doc in docs):
            raise TypeError("Expected all chunks to be strings")

        # Create embeddings for the text chunks
        embeddings = OpenAIEmbeddings()

        # Using Chroma as the vector store
        db = Chroma.from_texts(docs, embeddings)

        # Create a retriever
        retriever = db.as_retriever(search_type="mmr")

        logging.info("Retriever created successfully")

        return retriever

    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
        raise  # Re-raise the exception to propagate it

    except TypeError as type_error:
        logging.error(f"Type error: {type_error}")
        raise  # Re-raise the exception to propagate it

    except Exception as e:
        logging.error(f"Error creating retriever: {e}")
        raise  # Re-raise the exception to propagate it
