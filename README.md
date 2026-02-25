# VidRAG: YouTube Video Question Answering System

A powerful Retrieval-Augmented Generation (RAG) application that enables intelligent question-answering from YouTube videos using LLMs, LangChain, and OpenAI APIs.

## 🚀 Features

- **YouTube Video Processing**: Extract audio and transcripts from any YouTube video
- **Advanced RAG Pipeline**: Retrieval-Augmented Generation for accurate, context-aware responses
- **Vector Database Integration**: FAISS and ChromaDB support for efficient semantic search
- **NLP Preprocessing**: Text chunking, embeddings, and intelligent document processing
- **Interactive UI**: Beautiful Streamlit web interface with real-time querying
- **Production-Ready**: Modular architecture with error handling and logging

## 🛠️ Tech Stack

- **LLMs**: OpenAI GPT-3.5/GPT-4
- **Framework**: LangChain
- **Vector DBs**: FAISS, ChromaDB
- **UI**: Streamlit
- **APIs**: OpenAI, YouTube Transcript API
- **Processing**: Natural Language Processing, Text Embeddings

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection for YouTube access

## 🔧 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Vidrag
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Usage

1. **Run the Streamlit app**
```bash
streamlit run app.py
```

2. **Open your browser**
Navigate to `http://localhost:8501`

3. **Start asking questions**
- Enter a YouTube URL
- Wait for processing
- Ask questions about the video content
- Get AI-powered answers with sources

## 📁 Project Structure

```
Vidrag/
├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── youtube_processor.py   # YouTube transcript extraction
│   ├── text_processor.py      # Text chunking and preprocessing
│   ├── embeddings.py           # Embedding generation
│   ├── vector_store.py         # Vector database management
│   └── rag_pipeline.py         # RAG implementation
├── config/
│   └── config.py               # Configuration settings
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Utility functions
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                   # Project documentation
```

## 🎯 How It Works

1. **Video Input**: User provides YouTube URL
2. **Transcript Extraction**: Download and process video transcript
3. **Text Chunking**: Split transcript into semantic chunks
4. **Embedding Generation**: Create vector embeddings using OpenAI
5. **Vector Storage**: Store embeddings in FAISS/Chroma database
6. **Query Processing**: User asks a question
7. **Similarity Search**: Find relevant chunks using vector search
8. **Context Building**: Retrieve top-k relevant passages
9. **LLM Generation**: Generate answer using context and LLM
10. **Response**: Display answer with source references

## 🧪 Example Queries

- "What are the main topics discussed in this video?"
- "Can you explain the concept mentioned at the beginning?"
- "What solutions does the speaker propose?"
- "Summarize the key takeaways from this video"

## 🔒 Security

- Never commit your `.env` file
- Keep your OpenAI API key secure
- Use environment variables for sensitive data

## 📊 Performance

- Supports videos up to 2 hours
- Average processing time: 30-60 seconds
- Query response time: 2-5 seconds

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 🙏 Acknowledgments

- OpenAI for LLM APIs
- LangChain for RAG framework
- Streamlit for UI framework
- ChromaDB and FAISS for vector storage

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using RAG, LangChain, and OpenAI**
