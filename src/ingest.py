import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore

def main():
    print("Validating configuration...")
    Config.validate()
    
    print("Starting document ingestion from:", Config.DATA_PATH)
    
    # 1. Process and Chunk Documents
    processor = DocumentProcessor()
    chunks = processor.process()
    
    if not chunks:
        print("No documents found in the data directory. Exiting.")
        return
        
    # 2. Add to Vector Store
    print(f"Adding {len(chunks)} chunks to vector store at: {Config.CHROMA_PATH}")
    vector_store = VectorStore()
    vector_store.add_documents(chunks)
    
    print("✅ Ingestion complete! The database is ready for querying.")

if __name__ == "__main__":
    main()
