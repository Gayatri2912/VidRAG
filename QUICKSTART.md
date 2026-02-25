# VidRAG Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
VECTOR_STORE=chroma
```

### Step 3: Run the Application

```powershell
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Processing a Video

1. **Enter YouTube URL**: Paste any YouTube video URL with captions
2. **Click "Process Video"**: Wait 30-60 seconds for processing
3. **Video is Ready**: Green checkmarks indicate success

### Asking Questions

1. **Type Your Question**: In the text input field
2. **Click "Get Answer"**: RAG pipeline retrieves and generates answer
3. **View Sources**: Expand source sections to see relevant transcript chunks

## 🎯 Example Workflow

```python
# Behind the scenes, VidRAG does this:

# 1. Extract YouTube transcript
transcript = YouTubeProcessor.get_transcript(url)

# 2. Chunk the text
chunks = TextProcessor.chunk_text(transcript)

# 3. Create embeddings
embeddings = EmbeddingGenerator.generate_embeddings(chunks)

# 4. Store in vector database
VectorStore.create(chunks, embeddings)

# 5. Query with RAG
answer = RAGPipeline.query(question)
```

## 🔧 Configuration Options

### Vector Store
- **ChromaDB**: Persistent, disk-based (recommended)
- **FAISS**: In-memory, faster for single sessions

### Model Parameters
- **Temperature** (0.0-1.0): Controls creativity
  - Low (0.0-0.3): Factual, deterministic
  - High (0.7-1.0): Creative, varied
- **Max Tokens**: Response length (100-2000)
- **Top K**: Number of chunks to retrieve (1-10)

## 💡 Tips & Best Practices

### Video Selection
- ✅ Choose videos with **English captions**
- ✅ Educational/informational content works best
- ✅ Longer videos (10-60 min) provide richer context
- ❌ Avoid music videos without speech
- ❌ Avoid videos without captions

### Question Quality
- ✅ **Good**: "What are the three main strategies discussed for time management?"
- ✅ **Good**: "How does the speaker explain the concept of neural networks?"
- ❌ **Poor**: "What?" (too vague)
- ❌ **Poor**: "Tell me everything" (too broad)

### Performance Tips
1. Use **ChromaDB** for multiple queries on same video
2. Adjust **Top K** based on video length:
   - Short videos (<10 min): K=2-3
   - Medium videos (10-30 min): K=4-5
   - Long videos (>30 min): K=6-8
3. Lower **temperature** for factual Q&A
4. Higher **max tokens** for detailed explanations

## 🐛 Troubleshooting

### "No transcript found"
- Check if video has captions enabled
- Try different language options
- Some videos don't provide transcripts

### "API key invalid"
- Verify `.env` file exists
- Check OPENAI_API_KEY is correct
- Restart the Streamlit app

### "Out of memory"
- Use FAISS for very long videos
- Reduce chunk size in config
- Process shorter video segments

### Slow processing
- First-time processing takes longer
- Embeddings generation is the slow step
- Consider using ChromaDB for caching

## 📊 Understanding the Pipeline

### 1. YouTube Processing
```
Video URL → API Call → Transcript JSON → Text String
```

### 2. Text Processing
```
Raw Text → Clean → Chunk → Add Metadata → Documents
```

### 3. Embedding Generation
```
Documents → OpenAI API → Vector Embeddings → 1536-dim vectors
```

### 4. Vector Storage
```
Embeddings → FAISS/Chroma → Indexed → Searchable
```

### 5. RAG Query
```
Question → Embed → Search → Top K Chunks → LLM → Answer
```

## 🎓 Advanced Usage

### Custom Prompts
Modify the prompt template in `src/rag_pipeline.py`:

```python
custom_prompt = """
You are a helpful tutor. Explain concepts simply.
Context: {context}
Question: {question}
Answer:
"""
```

### Batch Processing
Process multiple videos programmatically:

```python
from src.youtube_processor import YouTubeProcessor
from src.vector_store import VectorStoreManager

urls = ['url1', 'url2', 'url3']
for url in urls:
    processor = YouTubeProcessor()
    transcript = processor.get_transcript(url)
    # ... continue processing
```

### Export Transcripts
Save transcripts for later use:

```python
import json

processor = YouTubeProcessor()
transcript = processor.get_transcript_with_timestamps(url)

with open('transcript.json', 'w') as f:
    json.dump(transcript, f)
```

## 🔐 Security Best Practices

1. **Never commit** `.env` file to Git
2. **Rotate** API keys regularly
3. **Monitor** API usage on OpenAI dashboard
4. **Limit** max tokens to control costs
5. **Use** environment variables for all secrets

## 📈 Monitoring & Costs

### OpenAI API Costs (Approximate)
- **Embeddings**: $0.0001 per 1K tokens
- **GPT-3.5-turbo**: $0.0015 per 1K tokens
- **Average video**: $0.05 - $0.20

### Token Usage
- 10-min video: ~5,000 tokens
- 30-min video: ~15,000 tokens
- 1-hour video: ~30,000 tokens

### Optimization
- Cache processed videos
- Reuse embeddings
- Limit max tokens per response
- Use GPT-3.5 instead of GPT-4

## 🤝 Contributing

Contributions welcome! Areas to improve:
- Support for more languages
- Audio extraction for videos without captions
- Video summarization features
- Chat history persistence
- Multi-video querying

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Streamlit Docs](https://docs.streamlit.io/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

---

**Need Help?** Open an issue on GitHub or check the documentation!
