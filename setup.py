"""
Setup and Installation Script for VidRAG
Run this script to set up the project environment
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is compatible")
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please update .env file with your OpenAI API key!")
        return True
    else:
        print("❌ .env.example template not found")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ['chroma_db', 'faiss_index', 'logs']
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Created directory: {dir_name}")
    
    return True

def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🎥  VidRAG Setup Script  🎥                      ║
    ║                                                          ║
    ║   YouTube Video Question Answering with RAG             ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("\n🚀 Starting setup process...\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if running in virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print("\n⚠️  Warning: Not running in a virtual environment!")
        print("It's recommended to use a virtual environment.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please activate a virtual environment and try again.")
            sys.exit(1)
    else:
        print("✅ Running in virtual environment")
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    if not run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    ):
        print("⚠️  Warning: Failed to upgrade pip, continuing...")
    
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing required packages"
    ):
        print("❌ Failed to install requirements!")
        sys.exit(1)
    
    # Create .env file
    print("\n📝 Setting up environment configuration...")
    create_env_file()
    
    # Create directories
    print("\n📁 Creating necessary directories...")
    create_directories()
    
    print("\n" + "="*60)
    print("✅ Setup completed successfully!")
    print("="*60)
    
    print("""
    
    📋 Next Steps:
    
    1. Open .env file and add your OpenAI API key:
       OPENAI_API_KEY=sk-your-key-here
    
    2. Run the application:
       streamlit run app.py
    
    3. Open your browser at:
       http://localhost:8501
    
    4. Read QUICKSTART.md for detailed usage guide
    
    📚 Documentation:
       - README.md - Project overview
       - QUICKSTART.md - Usage guide
       - .env.example - Configuration options
    
    🎉 Happy questioning!
    
    """)

if __name__ == "__main__":
    main()
