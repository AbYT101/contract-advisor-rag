import os
import logging
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import BM25Retriever
from langchain_core.documents import Document
from dotenv import load_dotenv, find_dotenv

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
        chunks = text_splitter.split_text(raw_text)

        # Ensure the chunks are a list of strings
        if not all(isinstance(chunk, str) for chunk in chunks):
            raise TypeError("Expected all chunks to be strings")

        # Create Document objects from the chunks with empty metadata
        docs = [Document(page_content=chunk, metadata={}) for chunk in chunks]

        # Create a BM25 retriever
        bm25_retriever = BM25Retriever(docs=docs)

        logging.info("Retriever created successfully")

        return bm25_retriever

    except Exception as e:
        logging.error(f"Error creating retriever: {e}")
        raise

    except Exception as e:
        logging.error(f"Error creating retriever: {e}")
        raise


