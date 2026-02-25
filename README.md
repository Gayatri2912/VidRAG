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


## 📄 License
 MIT License

## 🙏 Acknowledgments

- OpenAI for LLM APIs
- LangChain for RAG framework
- Streamlit for UI framework
- ChromaDB and FAISS for vector storage
<img width="1912" height="881" alt="Screenshot 2026-02-26 003617" src="https://github.com/user-attachments/assets/0345dc20-8137-4f8d-86fb-17678d909caf" />
<img width="1919" height="852" alt="Screenshot 2026-02-26 003626" src="https://github.com/user-attachments/assets/dd99e5c6-a84e-4646-ac5a-ca736e2b78fd" />
<img width="1917" height="893" alt="Screenshot 2026-02-26 003656" src="https://github.com/user-attachments/assets/e1c7032d-eef6-44e1-baef-1d261796f937" />

