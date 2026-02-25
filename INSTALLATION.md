# VidRAG Installation Guide

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Internet connection** (for YouTube access and API calls)
- **Git** (optional, for cloning)

## 🚀 Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Navigate to project directory**
```powershell
cd c:\Users\kaila\Desktop\Vidrag
```

2. **Create virtual environment**
```powershell
python -m venv venv
```

3. **Activate virtual environment**
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

4. **Run setup script**
```powershell
python setup.py
```

5. **Configure API key**
Edit `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

6. **Launch the app**
```powershell
streamlit run app.py
```

### Method 2: Manual Setup

1. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Upgrade pip**
```powershell
python -m pip install --upgrade pip
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Create .env file**
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```

Edit `.env` and add your API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

5. **Create directories**
```powershell
mkdir chroma_db
mkdir faiss_index
mkdir logs
```

6. **Run the application**
```powershell
streamlit run app.py
```

## 🔑 Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (you won't see it again!)
6. Add it to your `.env` file

## ✅ Verify Installation

### Test 1: Check Python Version
```powershell
python --version
# Should show Python 3.8 or higher
```

### Test 2: Check Installed Packages
```powershell
pip list | Select-String "streamlit|langchain|openai"
```

### Test 3: Run Test Script
```powershell
python test_installation.py
```

### Test 4: Launch Streamlit
```powershell
streamlit run app.py
```
Should open browser at `http://localhost:8501`

## 🐛 Troubleshooting

### Issue: "python is not recognized"
**Solution:** Python not in PATH. Reinstall Python and check "Add to PATH"

### Issue: "venv\Scripts\Activate.ps1 cannot be loaded"
**Solution:** PowerShell execution policy issue
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "pip: command not found"
**Solution:** 
```powershell
python -m ensurepip --upgrade
```

### Issue: "Failed to install requirements"
**Solution:** Install packages individually:
```powershell
pip install streamlit
pip install langchain
pip install langchain-openai
pip install chromadb
pip install youtube-transcript-api
pip install python-dotenv
```

### Issue: "OpenAI API key is required"
**Solution:** 
1. Check `.env` file exists in project root
2. Verify `OPENAI_API_KEY=` line has your key
3. No quotes around the key
4. Restart Streamlit after editing `.env`

### Issue: "No module named 'src'"
**Solution:** Run from project root directory:
```powershell
cd c:\Users\kaila\Desktop\Vidrag
streamlit run app.py
```

### Issue: "Transcript not available"
**Solution:** 
- Video must have captions/subtitles
- Try English videos with auto-generated captions
- Some videos disable transcript extraction

### Issue: Slow performance
**Solution:**
- First run is slower (downloads models)
- Use ChromaDB for persistence
- Reduce chunk size in config
- Check internet connection

## 📦 Package Versions

Key dependencies and compatible versions:

```
streamlit >= 1.31.0
langchain >= 0.1.10
openai >= 1.12.0
chromadb >= 0.4.22
faiss-cpu >= 1.7.4
youtube-transcript-api >= 0.6.2
python-dotenv >= 1.0.1
```

## 🔄 Updating

To update VidRAG to the latest version:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Update packages
pip install --upgrade -r requirements.txt

# Restart Streamlit
streamlit run app.py
```

## 🗑️ Uninstallation

To completely remove VidRAG:

```powershell
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
Remove-Item -Recurse -Force Vidrag
```

## 💻 System Requirements

### Minimum
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Storage: 500 MB free space
- OS: Windows 10/11, macOS 10.14+, Linux

### Recommended
- CPU: Quad-core 2.5 GHz+
- RAM: 8 GB+
- Storage: 2 GB free space
- SSD for faster vector database operations

## 🌐 Network Requirements

- Stable internet connection
- Access to:
  - `api.openai.com` (OpenAI API)
  - `youtube.com` (YouTube access)
  - `pypi.org` (package installation)

## 🔒 Security Considerations

1. **API Key Security**
   - Never commit `.env` to version control
   - Use environment variables in production
   - Rotate keys regularly

2. **Firewall Settings**
   - Allow Python and Streamlit through firewall
   - Only needed for localhost (127.0.0.1)

3. **Data Privacy**
   - Transcripts stored locally
   - No data sent except to OpenAI API
   - Vector databases stored on disk

## 📱 Alternative Installations

### Using Conda

```bash
conda create -n vidrag python=3.10
conda activate vidrag
pip install -r requirements.txt
```

### Using Docker (Advanced)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t vidrag .
docker run -p 8501:8501 vidrag
```

## 🎓 Next Steps

After successful installation:

1. **Read Documentation**
   - [README.md](README.md) - Project overview
   - [QUICKSTART.md](QUICKSTART.md) - Usage guide

2. **Try Examples**
   - Process a short educational video
   - Ask simple questions
   - Experiment with settings

3. **Explore Features**
   - Try both FAISS and ChromaDB
   - Adjust model parameters
   - Test with different video types

4. **Customize**
   - Modify prompts in `src/rag_pipeline.py`
   - Adjust chunk sizes in config
   - Customize UI in `app.py`

## 📞 Support

If you encounter issues:

1. Check Troubleshooting section above
2. Review error messages carefully
3. Search existing GitHub issues
4. Open a new issue with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)

---

**Installation Complete!** 🎉

Run `streamlit run app.py` to get started!
