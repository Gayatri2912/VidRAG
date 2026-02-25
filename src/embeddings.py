"""
Embedding generation using HuggingFace (free) or OpenAI
"""
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from config.config import Config
from utils.helpers import get_logger

logger = get_logger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for text using HuggingFace (free) or OpenAI"""
    
    def __init__(self, model: str = None):
        """
        Initialize embedding generator
        
        Args:
            model: Embedding model name (default from config)
        """
        if Config.USE_FREE_MODELS:
            # Use free HuggingFace embeddings
            self.model = model or Config.HUGGINGFACE_EMBEDDING_MODEL
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info(f"EmbeddingGenerator initialized with FREE HuggingFace model: {self.model}")
        else:
            # Use OpenAI embeddings
            self.model = model or Config.EMBEDDING_MODEL
            self.embeddings = OpenAIEmbeddings(
                model=self.model,
                openai_api_key=Config.OPENAI_API_KEY
            )
            logger.info(f"EmbeddingGenerator initialized with OpenAI model: {self.model}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query
        
        Args:
            query: Query string
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(query)
            logger.info(f"Generated query embedding")
            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise
    
    def get_embeddings_instance(self):
        """Get the LangChain embeddings instance"""
        return self.embeddings
