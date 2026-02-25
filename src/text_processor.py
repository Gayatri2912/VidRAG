"""
Text processing, chunking, and preprocessing
"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from utils.helpers import clean_text, get_logger
from config.config import Config

logger = get_logger(__name__)

class TextProcessor:
    """Handle text preprocessing and chunking"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize text processor
        
        Args:
            chunk_size: Size of each text chunk (default from config)
            chunk_overlap: Overlap between chunks (default from config)
        """
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        logger.info(f"TextProcessor initialized with chunk_size={self.chunk_size}, "
                   f"chunk_overlap={self.chunk_overlap}")
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess text
        
        Args:
            text: Raw text to process
            
        Returns:
            Cleaned text
        """
        # Clean text
        cleaned = clean_text(text)
        
        # Remove duplicate spaces
        cleaned = ' '.join(cleaned.split())
        
        logger.info(f"Preprocessed text: {len(text)} -> {len(cleaned)} characters")
        return cleaned
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[Document]:
        """
        Split text into chunks
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of Document objects with chunks
        """
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Create documents with metadata
        if metadata is None:
            metadata = {}
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(processed_text)
        
        # Create Document objects
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = {
                **metadata,
                'chunk_id': i,
                'total_chunks': len(chunks)
            }
            documents.append(Document(page_content=chunk, metadata=doc_metadata))
        
        logger.info(f"Created {len(documents)} chunks from text")
        return documents
    
    def chunk_transcript_with_timestamps(self, transcript: List[dict]) -> List[Document]:
        """
        Chunk transcript while preserving timestamps
        
        Args:
            transcript: List of transcript segments with timestamps
            
        Returns:
            List of Document objects with timestamp metadata
        """
        documents = []
        
        # Group segments into chunks
        current_chunk = []
        current_text = ""
        chunk_start_time = 0
        
        for segment in transcript:
            # Add segment to current chunk
            current_chunk.append(segment)
            current_text += " " + segment['text']
            
            # Check if chunk size reached
            if len(current_text) >= self.chunk_size:
                # Create document
                if current_chunk:
                    metadata = {
                        'start_time': current_chunk[0]['start'],
                        'end_time': current_chunk[-1]['start'] + current_chunk[-1]['duration'],
                        'chunk_id': len(documents)
                    }
                    documents.append(Document(
                        page_content=current_text.strip(),
                        metadata=metadata
                    ))
                
                # Reset for next chunk
                current_chunk = []
                current_text = ""
        
        # Add remaining chunk
        if current_chunk:
            metadata = {
                'start_time': current_chunk[0]['start'],
                'end_time': current_chunk[-1]['start'] + current_chunk[-1]['duration'],
                'chunk_id': len(documents)
            }
            documents.append(Document(
                page_content=current_text.strip(),
                metadata=metadata
            ))
        
        logger.info(f"Created {len(documents)} chunks with timestamps")
        return documents
    
    def get_chunk_statistics(self, documents: List[Document]) -> dict:
        """
        Get statistics about chunks
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary with statistics
        """
        if not documents:
            return {}
        
        chunk_sizes = [len(doc.page_content) for doc in documents]
        
        return {
            'num_chunks': len(documents),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'total_characters': sum(chunk_sizes)
        }
