import os
import logging
from typing import List
from collections import Counter
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
from rank_bm25 import BM25Okapi  # You may need to install the rank_bm25 package

load_dotenv(find_dotenv())

DATA_DIR = 'data/texts'
KNOWLEDGE_FILE = 'knowledge.txt'

class CombinedRetriever:
    def __init__(self, bm25_retriever, cosine_retriever, docs):
        self.bm25_retriever = bm25_retriever
        self.cosine_retriever = cosine_retriever
        self.docs = docs

    def retrieve(self, query: str, top_k: int = 10) -> List[str]:
        # Tokenize the query for BM25
        tokenized_query = query.split()

        # Get BM25 scores
        top_k_bm25_indices = self.bm25_retriever.get_top_n(tokenized_query, self.docs, n=top_k)

        # Get cosine similarity scores
        cosine_results = self.cosine_retriever.retrieve(query)
        cosine_indices = [self.docs.index(doc) for doc in cosine_results]

        # Combine the results (simple voting)
        combined_results = top_k_bm25_indices + cosine_indices
        combined_counter = Counter(combined_results)
        combined_top_k = [self.docs[idx] for idx, _ in combined_counter.most_common(top_k)]

        return combined_top_k

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
        embedded_docs = embeddings.embed_documents(docs)

        # Using Chroma as the vector store for cosine similarity
        db_cosine = Chroma.from_texts(docs, embeddings)
        retriever_cosine = db_cosine.as_retriever(search_type="mmr")

        # Create BM25 retriever
        tokenized_docs = [doc.split() for doc in docs]
        bm25 = BM25Okapi(tokenized_docs)

        logging.info("Retrievers created successfully")

        combined_retriever = CombinedRetriever(bm25, retriever_cosine, docs)
        return combined_retriever

    except Exception as e:
        logging.error(f"Error creating retriever: {e}")
        raise

