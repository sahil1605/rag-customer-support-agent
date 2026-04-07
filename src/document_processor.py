import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config

class DocumentProcessor:
    def __init__(self, data_path=Config.DATA_PATH):
        self.data_path = data_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def load_documents(self):
        """Loads all supported documents from the data directory."""
        documents = []
        
        # Load Markdown files
        md_loader = DirectoryLoader(
            self.data_path, 
            glob="**/*.md", 
            loader_cls=TextLoader
        )
        documents.extend(md_loader.load())
        
        # Load PDF files if any
        pdf_loader = DirectoryLoader(
            self.data_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents.extend(pdf_loader.load())
        
        return documents

    def split_documents(self, documents):
        """Splits documents into smaller optimize chunks."""
        return self.text_splitter.split_documents(documents)

    def process(self):
        """Loads and splits documents, returning chunks."""
        docs = self.load_documents()
        chunks = self.split_documents(docs)
        print(f"Loaded {len(docs)} documents and split them into {len(chunks)} chunks.")
        return chunks
