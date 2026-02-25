"""
RAG (Retrieval-Augmented Generation) pipeline implementation
"""
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from config.config import Config
from src.vector_store import VectorStoreManager
from utils.helpers import get_logger, format_timestamp

logger = get_logger(__name__)

class RAGPipeline:
    """RAG pipeline for question answering"""
    
    # Default prompt template
    DEFAULT_PROMPT_TEMPLATE = """You are an AI assistant helping users understand YouTube video content. 
Use the following pieces of context from the video transcript to answer the question. 
If you don't know the answer based on the context, say so - don't make up information.

Context:
{context}

Question: {question}

Please provide a clear, accurate answer based on the video content:"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        """
        Initialize RAG pipeline
        
        Args:
            vector_store_manager: Vector store manager instance
        """
        self.vector_store_manager = vector_store_manager
        
        # Initialize LLM (free local HuggingFace or OpenAI)
        if Config.USE_FREE_MODELS:
            logger.info(f"Loading FREE local HuggingFace model: {Config.HUGGINGFACE_LLM_MODEL}")
            # Load local model
            tokenizer = AutoTokenizer.from_pretrained(Config.HUGGINGFACE_LLM_MODEL)
            model = AutoModelForSeq2SeqLM.from_pretrained(Config.HUGGINGFACE_LLM_MODEL)
            
            # Create pipeline
            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
                device=-1  # CPU
            )
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
            logger.info(f"Using FREE local LLM: {Config.HUGGINGFACE_LLM_MODEL}")
        else:
            self.llm = ChatOpenAI(
                model=Config.OPENAI_MODEL,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                openai_api_key=Config.OPENAI_API_KEY
            )
            logger.info(f"Using OpenAI LLM: {Config.OPENAI_MODEL}")
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            template=self.DEFAULT_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        # Initialize retrieval QA chain
        self.qa_chain = None
        self._setup_qa_chain()
        
        logger.info("RAGPipeline initialized")
    
    def _setup_qa_chain(self) -> None:
        """Setup the retrieval QA chain"""
        vector_store = self.vector_store_manager.get_vector_store()
        
        if not vector_store:
            logger.warning("Vector store not initialized. QA chain not created.")
            return
        
        try:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(
                    search_kwargs={"k": Config.TOP_K_RESULTS}
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt_template}
            )
            logger.info("QA chain setup complete")
        except Exception as e:
            logger.error(f"Error setting up QA chain: {str(e)}")
            raise
    
    def query(self, question: str) -> Dict:
        """
        Query the RAG pipeline
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.qa_chain:
            self._setup_qa_chain()
        
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Ensure vector store is created.")
        
        try:
            logger.info(f"Processing query: {question}")
            
            # Get response from QA chain
            response = self.qa_chain.invoke({"query": question})
            
            # Extract answer and sources
            answer = response.get('result', '')
            source_documents = response.get('source_documents', [])
            
            # Format response
            result = {
                'answer': answer,
                'sources': self._format_sources(source_documents),
                'num_sources': len(source_documents)
            }
            
            logger.info(f"Query processed successfully with {len(source_documents)} sources")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    def _format_sources(self, documents: List[Document]) -> List[Dict]:
        """
        Format source documents for display
        
        Args:
            documents: List of source documents
            
        Returns:
            List of formatted source dictionaries
        """
        formatted_sources = []
        
        for i, doc in enumerate(documents):
            source = {
                'chunk_id': i + 1,
                'content': doc.page_content,
                'metadata': doc.metadata
            }
            
            # Add timestamp if available
            if 'start_time' in doc.metadata:
                source['timestamp'] = format_timestamp(doc.metadata['start_time'])
            
            formatted_sources.append(source)
        
        return formatted_sources
    
    def query_with_custom_prompt(self, question: str, custom_prompt: str) -> Dict:
        """
        Query with a custom prompt template
        
        Args:
            question: User question
            custom_prompt: Custom prompt template
            
        Returns:
            Dictionary with answer and sources
        """
        # Create custom prompt template
        custom_template = PromptTemplate(
            template=custom_prompt,
            input_variables=["context", "question"]
        )
        
        # Create temporary QA chain with custom prompt
        vector_store = self.vector_store_manager.get_vector_store()
        
        custom_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_kwargs={"k": Config.TOP_K_RESULTS}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": custom_template}
        )
        
        # Get response
        response = custom_chain.invoke({"query": question})
        
        return {
            'answer': response.get('result', ''),
            'sources': self._format_sources(response.get('source_documents', [])),
            'num_sources': len(response.get('source_documents', []))
        }
    
    def get_relevant_chunks(self, query: str, k: int = None) -> List[Document]:
        """
        Get relevant chunks without generating an answer
        
        Args:
            query: Search query
            k: Number of chunks to retrieve
            
        Returns:
            List of relevant documents
        """
        return self.vector_store_manager.similarity_search(query, k=k)
    
    def update_llm_settings(self, temperature: float = None, max_tokens: int = None):
        """
        Update LLM settings
        
        Args:
            temperature: Model temperature
            max_tokens: Maximum tokens in response
        """
        if temperature is not None:
            self.llm.temperature = temperature
        if max_tokens is not None:
            self.llm.max_tokens = max_tokens
        
        # Recreate QA chain with new settings
        self._setup_qa_chain()
        logger.info(f"Updated LLM settings: temperature={temperature}, max_tokens={max_tokens}")
