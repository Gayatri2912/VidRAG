"""
VidRAG - YouTube Video Question Answering System
Main Streamlit Application
"""
import streamlit as st
from typing import Optional
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from src.youtube_processor import YouTubeProcessor
from src.text_processor import TextProcessor
from src.vector_store import VectorStoreManager
from src.rag_pipeline import RAGPipeline
from utils.helpers import validate_youtube_url, get_logger

logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF0000;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF0000;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #FF0000;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 3px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize Streamlit session state variables"""
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'video_url' not in st.session_state:
        st.session_state.video_url = None
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    if 'transcript_length' not in st.session_state:
        st.session_state.transcript_length = 0
    if 'num_chunks' not in st.session_state:
        st.session_state.num_chunks = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def process_video(video_url: str, vector_store_type: str = 'chroma') -> bool:
    """
    Process YouTube video and create vector store
    
    Args:
        video_url: YouTube video URL
        vector_store_type: Type of vector store to use
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with st.spinner("🎥 Extracting transcript from YouTube..."):
            # Extract transcript
            youtube_processor = YouTubeProcessor()
            transcript = youtube_processor.get_transcript(video_url)
            
            if not transcript:
                st.error("❌ Failed to extract transcript. Please check if the video has captions enabled.")
                return False
            
            st.session_state.transcript_length = len(transcript)
            st.success(f"✅ Transcript extracted: {len(transcript):,} characters")
        
        with st.spinner("📝 Processing and chunking text..."):
            # Process and chunk text
            text_processor = TextProcessor()
            documents = text_processor.chunk_text(
                transcript,
                metadata={'source': video_url, 'type': 'youtube_transcript'}
            )
            
            st.session_state.num_chunks = len(documents)
            st.success(f"✅ Created {len(documents)} text chunks")
        
        with st.spinner("🧠 Generating embeddings and creating vector store..."):
            # Create vector store
            vector_store_manager = VectorStoreManager(store_type=vector_store_type)
            vector_store_manager.create_vector_store(documents)
            st.success(f"✅ Vector store created using {vector_store_type.upper()}")
        
        with st.spinner("🤖 Initializing RAG pipeline..."):
            # Initialize RAG pipeline
            rag_pipeline = RAGPipeline(vector_store_manager)
            st.session_state.rag_pipeline = rag_pipeline
            st.success("✅ RAG pipeline ready!")
        
        st.session_state.processed = True
        st.session_state.video_url = video_url
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        logger.error(f"Error processing video: {str(e)}")
        return False

def display_answer(result: dict):
    """Display the answer with sources"""
    # Display answer
    st.markdown("### 🎯 Answer")
    st.markdown(f"<div style='background-color: #e8f4f8; padding: 1rem; border-radius: 5px; margin: 1rem 0;'>"
                f"{result['answer']}</div>", unsafe_allow_html=True)
    
    # Display sources
    if result['sources']:
        st.markdown("### 📚 Sources from Transcript")
        for i, source in enumerate(result['sources'], 1):
            with st.expander(f"Source {i} {source.get('timestamp', '')}"):
                st.write(source['content'])
                if 'metadata' in source:
                    st.caption(f"Metadata: {source['metadata']}")

def main():
    """Main application function"""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown("<h1 class='main-header'>🎥 VidRAG</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>YouTube Video Question Answering with RAG</p>", unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check configuration
        try:
            Config.validate()
            if Config.USE_FREE_MODELS:
                st.success("✅ Using FREE HuggingFace Models")
                st.info("🤗 Embeddings: " + Config.HUGGINGFACE_EMBEDDING_MODEL.split('/')[-1])
            else:
                st.success("✅ OpenAI API Key configured")
        except ValueError as e:
            st.error(str(e))
            st.info("Please set your OPENAI_API_KEY in the .env file")
            st.stop()
        
        st.divider()
        
        # Vector store selection
        st.subheader("Vector Database")
        vector_store_type = st.selectbox(
            "Select Vector Store",
            options=['chroma', 'faiss'],
            index=0,
            help="Choose between ChromaDB (persistent) or FAISS (in-memory)"
        )
        
        st.divider()
        
        # Model settings
        st.subheader("Model Settings")
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=Config.TEMPERATURE,
            step=0.1,
            help="Higher values make output more creative"
        )
        
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=2000,
            value=Config.MAX_TOKENS,
            step=100,
            help="Maximum length of response"
        )
        
        top_k = st.slider(
            "Top K Results",
            min_value=1,
            max_value=10,
            value=Config.TOP_K_RESULTS,
            help="Number of relevant chunks to retrieve"
        )
        
        # Update config
        Config.TEMPERATURE = temperature
        Config.MAX_TOKENS = max_tokens
        Config.TOP_K_RESULTS = top_k
        
        st.divider()
        
        # Info
        st.subheader("📊 Status")
        if st.session_state.processed:
            st.success("✅ Video Processed")
            st.metric("Transcript Length", f"{st.session_state.transcript_length:,} chars")
            st.metric("Text Chunks", st.session_state.num_chunks)
        else:
            st.info("⏳ No video processed yet")
    
    # Main content
    st.header("🎬 Step 1: Process YouTube Video")
    
    # Video URL input
    col1, col2 = st.columns([3, 1])
    with col1:
        video_url = st.text_input(
            "Enter YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste a YouTube video URL with captions/subtitles"
        )
    
    with col2:
        st.write("")
        st.write("")
        process_button = st.button("🚀 Process Video", type="primary")
    
    # Process video
    if process_button:
        if not video_url:
            st.warning("⚠️ Please enter a YouTube URL")
        elif not validate_youtube_url(video_url):
            st.error("❌ Invalid YouTube URL. Please check and try again.")
        else:
            success = process_video(video_url, vector_store_type)
            if success:
                st.balloons()
    
    # Show example URLs
    with st.expander("📺 Example YouTube URLs"):
        st.markdown("""
        Try these example videos:
        - Educational: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        - Technology: https://www.youtube.com/watch?v=...
        
        **Note:** Video must have English captions/subtitles enabled
        """)
    
    st.divider()
    
    # Question answering section
    if st.session_state.processed:
        st.header("💬 Step 2: Ask Questions")
        
        # Question input
        user_question = st.text_input(
            "Ask a question about the video",
            placeholder="What is the main topic discussed in this video?",
            help="Enter your question about the video content"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("🔍 Get Answer", type="primary")
        with col2:
            clear_button = st.button("🗑️ Clear History")
        
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
        
        # Process question
        if ask_button and user_question:
            with st.spinner("🤔 Thinking..."):
                try:
                    # Update RAG settings
                    st.session_state.rag_pipeline.update_llm_settings(
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    # Get answer
                    result = st.session_state.rag_pipeline.query(user_question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'question': user_question,
                        'answer': result
                    })
                    
                    # Display answer
                    display_answer(result)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Display chat history
        if st.session_state.chat_history:
            st.divider()
            st.header("📜 Chat History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
                with st.container():
                    st.markdown(f"**Q{len(st.session_state.chat_history) - i + 1}:** {chat['question']}")
                    st.markdown(f"**A:** {chat['answer']['answer']}")
                    st.caption(f"Sources used: {chat['answer']['num_sources']}")
                    st.divider()
        
        # Suggested questions
        st.header("💡 Suggested Questions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 What are the main topics?"):
                st.session_state.suggested_question = "What are the main topics discussed in this video?"
        
        with col2:
            if st.button("🎯 Summarize the video"):
                st.session_state.suggested_question = "Please provide a comprehensive summary of this video."
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("🔑 What are the key takeaways?"):
                st.session_state.suggested_question = "What are the key takeaways from this video?"
        
        with col4:
            if st.button("❓ What questions are answered?"):
                st.session_state.suggested_question = "What questions or problems does this video address?"
    
    else:
        st.info("👆 Please process a YouTube video first to start asking questions")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>VidRAG</strong> - Powered by OpenAI, LangChain, and Streamlit</p>
        <p>🔒 Your API key is secure | 🚀 Built with RAG Technology | 💡 Open Source</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
