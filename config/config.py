"""
Configuration settings for VidRAG application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Model Configuration
    USE_FREE_MODELS = os.getenv('USE_FREE_MODELS', 'true').lower() == 'true'
    
    # OpenAI Configuration (optional if USE_FREE_MODELS=true)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002')
    
    # HuggingFace Free Models
    HUGGINGFACE_EMBEDDING_MODEL = os.getenv('HUGGINGFACE_EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    HUGGINGFACE_LLM_MODEL = os.getenv('HUGGINGFACE_LLM_MODEL', 'google/flan-t5-large')
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '')
    
    # LangChain Configuration (optional)
    LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'false').lower() == 'true'
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', '')
    
    # Vector Store Configuration
    VECTOR_STORE = os.getenv('VECTOR_STORE', 'chroma')  # Options: chroma, faiss
    CHROMA_DB_DIR = './chroma_db'
    FAISS_INDEX_PATH = './faiss_index'
    
    # Text Processing Configuration
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    
    # RAG Configuration
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', 4))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 500))
    
    # Streamlit Configuration
    PAGE_TITLE = "VidRAG - YouTube Q&A"
    PAGE_ICON = "🎥"
    LAYOUT = "wide"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.USE_FREE_MODELS and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when USE_FREE_MODELS=false. Please set it in .env file")
        return True
