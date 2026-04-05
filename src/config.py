import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    """Project configuration management."""
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "storage/chroma_db")
    DATA_PATH = os.getenv("DATA_PATH", "data/")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")

    @classmethod
    def validate(cls):
        """Validates that critical configurations are present."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY must be set in .env file.")
        
        # Ensure directories exist
        os.makedirs(cls.DATA_PATH, exist_ok=True)
        os.makedirs(os.path.dirname(cls.CHROMA_PATH) or ".", exist_ok=True)
