import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import Config

class VectorStore:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.persist_directory = Config.CHROMA_PATH

    def get_db(self):
        """Returns the ChromaDB instance."""
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(self, chunks):
        """Adds document chunks to the vector database."""
        db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        # Note: In newer chromadb versions, it automatically persists upon creation/modification.
        return db
