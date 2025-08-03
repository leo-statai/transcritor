"""
Audio extraction module for video files.
"""
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from utils import is_video_file, get_file_extension, cleanup_temp_files


class AudioExtractor:
    """Handles audio extraction from video files and audio normalization."""
    
    def __init__(self):
        self.temp_files = []
    
    def process(self, input_path: Path) -> Path:
        """
        Process input file and return path to audio file.
        If input is video, extract audio. If audio, return as-is.
        """
        if is_video_file(input_path):
            return self.extract_from_video(input_path)
        else:
            return input_path
    
    def extract_from_video(self, video_path: Path) -> Path:
        """Extract audio from video file using FFmpeg."""
        # Create temporary audio file
        temp_audio = Path(tempfile.mktemp(suffix='.wav'))
        self.temp_files.append(temp_audio)
        
        try:
            # Use FFmpeg to extract audio
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # PCM 16-bit
                '-ar', '16000',  # 16kHz sample rate (optimal for Whisper)
                '-ac', '1',  # Mono
                '-y',  # Overwrite output file
                str(temp_audio)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if not temp_audio.exists():
                raise RuntimeError("Falha na extração de áudio")
            
            return temp_audio
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro no FFmpeg: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "FFmpeg não encontrado. Instale com: "
                "sudo apt install ffmpeg (Ubuntu/Debian) ou "
                "brew install ffmpeg (macOS)"
            )
    
    def get_audio_format(self, audio_path: Path) -> dict:
        """Get audio file information using FFprobe."""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(audio_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            return json.loads(result.stdout)
            
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return {}
    
    def normalize_audio(self, audio_path: Path) -> Path:
        """
        Normalize audio for better transcription quality.
        Returns path to normalized audio file.
        """
        if is_video_file(audio_path.parent.parent):
            # Already extracted and normalized
            return audio_path
        
        # Create temporary normalized audio file
        temp_normalized = Path(tempfile.mktemp(suffix='.wav'))
        self.temp_files.append(temp_normalized)
        
        try:
            cmd = [
                'ffmpeg',
                '-i', str(audio_path),
                '-acodec', 'pcm_s16le',
                '-ar', '16000',  # 16kHz for Whisper
                '-ac', '1',      # Mono
                '-af', 'volume=1.5',  # Slight volume boost
                '-y',
                str(temp_normalized)
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            if not temp_normalized.exists():
                return audio_path  # Return original if normalization fails
            
            return temp_normalized
            
        except subprocess.CalledProcessError:
            return audio_path  # Return original if normalization fails
    
    def cleanup(self) -> None:
        """Clean up temporary files."""
        cleanup_temp_files(*self.temp_files)
        self.temp_files.clear()
    
    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup()