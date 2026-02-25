"""
Test Installation Script
Verify that all components are installed correctly
"""
import sys
import os

def test_python_version():
    """Test Python version"""
    print("\n1. Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def test_imports():
    """Test required package imports"""
    print("\n2. Testing package imports...")
    packages = {
        'streamlit': 'streamlit',
        'langchain': 'langchain',
        'langchain_openai': 'langchain-openai',
        'chromadb': 'chromadb',
        'faiss': 'faiss-cpu',
        'youtube_transcript_api': 'youtube-transcript-api',
        'dotenv': 'python-dotenv',
        'openai': 'openai'
    }
    
    failed = []
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package} - OK")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            failed.append(package)
    
    return len(failed) == 0

def test_project_structure():
    """Test project structure"""
    print("\n3. Testing project structure...")
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        'config/config.py',
        'src/__init__.py',
        'src/youtube_processor.py',
        'src/text_processor.py',
        'src/embeddings.py',
        'src/vector_store.py',
        'src/rag_pipeline.py',
        'utils/helpers.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - OK")
        else:
            print(f"   ❌ {file} - MISSING")
            missing.append(file)
    
    return len(missing) == 0

def test_env_file():
    """Test environment configuration"""
    print("\n4. Testing environment configuration...")
    
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        
        # Check if API key is set
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            print("   ✅ OpenAI API key is configured")
            return True
        else:
            print("   ⚠️  OpenAI API key not set in .env file")
            print("   📝 Please add your API key to .env file")
            return False
    else:
        print("   ❌ .env file not found")
        print("   📝 Copy .env.example to .env and add your API key")
        return False

def test_modules():
    """Test custom modules"""
    print("\n5. Testing custom modules...")
    
    try:
        # Add project root to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from config.config import Config
        print("   ✅ config.config - OK")
        
        from src.youtube_processor import YouTubeProcessor
        print("   ✅ src.youtube_processor - OK")
        
        from src.text_processor import TextProcessor
        print("   ✅ src.text_processor - OK")
        
        from src.embeddings import EmbeddingGenerator
        print("   ✅ src.embeddings - OK")
        
        from src.vector_store import VectorStoreManager
        print("   ✅ src.vector_store - OK")
        
        from src.rag_pipeline import RAGPipeline
        print("   ✅ src.rag_pipeline - OK")
        
        from utils.helpers import get_logger, extract_video_id
        print("   ✅ utils.helpers - OK")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Module import failed: {str(e)}")
        return False

def test_youtube_extraction():
    """Test YouTube video ID extraction"""
    print("\n6. Testing YouTube URL parsing...")
    
    try:
        from utils.helpers import extract_video_id, validate_youtube_url
        
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
        ]
        
        for url in test_urls:
            video_id = extract_video_id(url)
            is_valid = validate_youtube_url(url)
            if video_id and is_valid:
                print(f"   ✅ Parsed {url[:40]}... → {video_id}")
            else:
                print(f"   ❌ Failed to parse: {url}")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ URL parsing failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("VidRAG Installation Test")
    print("="*60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Environment Config", test_env_file),
        ("Custom Modules", test_modules),
        ("YouTube Parsing", test_youtube_extraction),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Test failed with error: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Installation is complete.")
        print("\nNext steps:")
        print("1. Ensure your OpenAI API key is in .env file")
        print("2. Run: streamlit run app.py")
        print("3. Open browser at http://localhost:8501")
    else:
        print("\n⚠️  Some tests failed. Please review errors above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Copy .env.example to .env")
        print("- Add your OpenAI API key to .env")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
