"""
YouTube video processing and transcript extraction
"""
from typing import Optional, List, Dict
import subprocess
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from utils.helpers import extract_video_id, get_logger

logger = get_logger(__name__)

class YouTubeProcessor:
    """Handle YouTube video transcript extraction and processing"""
    
    def __init__(self):
        self.video_id = None
        self.transcript = None
    
    def _get_transcript_ytdlp(self, video_url: str) -> Optional[str]:
        """
        Fallback method using yt-dlp to extract subtitles
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Transcript text or None
        """
        try:
            logger.info("Trying yt-dlp method...")
            
            # Use yt-dlp to get subtitles in SRT format (simpler to parse)
            cmd = [
                'yt-dlp',
                '--skip-download',
                '--write-auto-subs',
                '--sub-lang', 'en',
                '--sub-format', 'srt',
                '--convert-subs', 'srt',
                '--output', 'temp_subtitle',
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd='.')
            
            # Read the generated subtitle file
            import os
            import re
            
            subtitle_files = ['temp_subtitle.en.srt', 'temp_subtitle.en-orig.srt']
            subtitle_content = None
            
            for subtitle_file in subtitle_files:
                if os.path.exists(subtitle_file):
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        subtitle_content = f.read()
                    os.remove(subtitle_file)  # Clean up
                    break
            
            if subtitle_content:
                # Parse SRT format and extract text
                # Remove timing lines and sequence numbers
                lines = subtitle_content.split('\n')
                transcript_text = []
                
                for line in lines:
                    line = line.strip()
                    # Skip empty lines, numbers, and timestamp lines
                    if line and not line.isdigit() and '-->' not in line:
                        # Remove HTML tags
                        line = re.sub(r'<[^>]+>', '', line)
                        transcript_text.append(line)
                
                full_text = ' '.join(transcript_text)
                logger.info(f"yt-dlp: Extracted {len(full_text)} characters")
                return full_text
                
        except Exception as e:
            logger.error(f"yt-dlp method failed: {str(e)}")
        
        return None
        
    def get_transcript(self, video_url: str, languages: List[str] = ['en']) -> Optional[str]:
        """
        Extract transcript from YouTube video
        
        Args:
            video_url: YouTube video URL
            languages: List of preferred languages (default: ['en'])
            
        Returns:
            Complete transcript text or None if failed
        """
        try:
            # Extract video ID
            self.video_id = extract_video_id(video_url)
            if not self.video_id:
                logger.error(f"Invalid YouTube URL: {video_url}")
                return None
            
            logger.info(f"Extracting transcript for video ID: {self.video_id}")
            
            # Try primary method first
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    self.video_id,
                    languages=languages
                )
                
                # Combine all transcript segments
                self.transcript = transcript_list
                full_text = ' '.join([segment['text'] for segment in transcript_list])
                
                logger.info(f"Successfully extracted transcript ({len(full_text)} characters)")
                return full_text
                
            except Exception as api_error:
                logger.warning(f"Primary API failed: {str(api_error)}")
                logger.info("Trying fallback method with yt-dlp...")
                
                # Try fallback method
                fallback_text = self._get_transcript_ytdlp(video_url)
                if fallback_text:
                    return fallback_text
                    
                raise api_error
            
        except TranscriptsDisabled:
            logger.error("Transcripts are disabled for this video")
            return None
        except NoTranscriptFound:
            logger.error(f"No transcript found for languages: {languages}")
            return None
        except Exception as e:
            logger.error(f"Error extracting transcript: {str(e)}")
            return None
    
    def get_transcript_with_timestamps(self, video_url: str, languages: List[str] = ['en']) -> Optional[List[Dict]]:
        """
        Extract transcript with timestamp information
        
        Args:
            video_url: YouTube video URL
            languages: List of preferred languages
            
        Returns:
            List of transcript segments with timestamps
        """
        try:
            self.video_id = extract_video_id(video_url)
            if not self.video_id:
                return None
            
            transcript_list = YouTubeTranscriptApi.get_transcript(
                self.video_id,
                languages=languages
            )
            
            self.transcript = transcript_list
            return transcript_list
            
        except Exception as e:
            logger.error(f"Error extracting transcript with timestamps: {str(e)}")
            return None
    
    def get_available_transcripts(self, video_url: str) -> List[str]:
        """
        Get list of available transcript languages
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            List of available language codes
        """
        try:
            self.video_id = extract_video_id(video_url)
            if not self.video_id:
                return []
            
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
            return [transcript.language_code for transcript in transcript_list]
            
        except Exception as e:
            logger.error(f"Error listing transcripts: {str(e)}")
            return []
    
    def search_transcript(self, query: str, context_size: int = 50) -> List[Dict]:
        """
        Search for specific text in transcript
        
        Args:
            query: Search query
            context_size: Number of characters around match
            
        Returns:
            List of matches with context
        """
        if not self.transcript:
            return []
        
        results = []
        query_lower = query.lower()
        
        for segment in self.transcript:
            text = segment['text']
            if query_lower in text.lower():
                results.append({
                    'timestamp': segment['start'],
                    'text': text,
                    'duration': segment['duration']
                })
        
        return results
