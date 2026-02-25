"""
Utility functions for VidRAG application
"""
import re
import logging
from typing import Optional
from urllib.parse import urlparse, parse_qs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from URL
    
    Supports formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    # Regular YouTube URL
    if 'youtube.com' in url:
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            return params.get('v', [None])[0]
    
    # Short YouTube URL
    elif 'youtu.be' in url:
        parsed = urlparse(url)
        return parsed.path.strip('/')
    
    # Embedded URL
    elif 'youtube.com/embed' in url:
        parsed = urlparse(url)
        return parsed.path.split('/')[2] if len(parsed.path.split('/')) > 2 else None
    
    return None

def validate_youtube_url(url: str) -> bool:
    """Validate if URL is a valid YouTube URL"""
    video_id = extract_video_id(url)
    return video_id is not None and len(video_id) == 11

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
