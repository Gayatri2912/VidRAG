"""
Vector store management for FAISS and ChromaDB
"""
from typing import List, Optional
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.documents import Document
from config.config import Config
from src.embeddings import EmbeddingGenerator
from utils.helpers import get_logger
import os

logger = get_logger(__name__)

class VectorStoreManager:
    """Manage vector databases (FAISS and ChromaDB)"""
    
    def __init__(self, store_type: str = None):
        """
        Initialize vector store manager
        
        Args:
            store_type: Type of vector store ('faiss' or 'chroma')
        """
        self.store_type = store_type or Config.VECTOR_STORE
        self.vector_store = None
        self.embedding_generator = EmbeddingGenerator()
        
        logger.info(f"VectorStoreManager initialized with {self.store_type}")
    
    def create_vector_store(self, documents: List[Document]) -> None:
        """
        Create vector store from documents
        
        Args:
            documents: List of Document objects
        """
        try:
            embeddings = self.embedding_generator.get_embeddings_instance()
            
            if self.store_type == 'faiss':
                self.vector_store = FAISS.from_documents(
                    documents=documents,
                    embedding=embeddings
                )
                logger.info(f"Created FAISS vector store with {len(documents)} documents")
                
            elif self.store_type == 'chroma':
                # Create ChromaDB directory if it doesn't exist
                os.makedirs(Config.CHROMA_DB_DIR, exist_ok=True)
                
                self.vector_store = Chroma.from_documents(
                    documents=documents,
                    embedding=embeddings,
                    persist_directory=Config.CHROMA_DB_DIR
                )
                logger.info(f"Created Chroma vector store with {len(documents)} documents")
            
            else:
                raise ValueError(f"Unsupported vector store type: {self.store_type}")
                
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to existing vector store
        
        Args:
            documents: List of Document objects
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        try:
            self.vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")
        
        k = k or Config.TOP_K_RESULTS
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            raise
    
    def similarity_search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """
        Search for similar documents with relevance scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")
        
        k = k or Config.TOP_K_RESULTS
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} similar documents with scores")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search with score: {str(e)}")
            raise
    
    def save(self, path: str = None) -> None:
        """
        Save vector store to disk
        
        Args:
            path: Path to save the vector store
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")
        
        try:
            if self.store_type == 'faiss':
                save_path = path or Config.FAISS_INDEX_PATH
                self.vector_store.save_local(save_path)
                logger.info(f"Saved FAISS vector store to {save_path}")
                
            elif self.store_type == 'chroma':
                # ChromaDB persists automatically
                logger.info(f"Chroma vector store persisted to {Config.CHROMA_DB_DIR}")
                
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load(self, path: str = None) -> None:
        """
        Load vector store from disk
        
        Args:
            path: Path to load the vector store from
        """
        try:
            embeddings = self.embedding_generator.get_embeddings_instance()
            
            if self.store_type == 'faiss':
                load_path = path or Config.FAISS_INDEX_PATH
                self.vector_store = FAISS.load_local(
                    load_path,
                    embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded FAISS vector store from {load_path}")
                
            elif self.store_type == 'chroma':
                load_path = path or Config.CHROMA_DB_DIR
                self.vector_store = Chroma(
                    persist_directory=load_path,
                    embedding_function=embeddings
                )
                logger.info(f"Loaded Chroma vector store from {load_path}")
                
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
    
    def delete(self) -> None:
        """Delete the vector store"""
        if self.store_type == 'chroma' and self.vector_store:
            try:
                self.vector_store.delete_collection()
                logger.info("Deleted Chroma collection")
            except Exception as e:
                logger.error(f"Error deleting vector store: {str(e)}")
        
        self.vector_store = None
    
    def get_vector_store(self):
        """Get the vector store instance"""
        return self.vector_store
