"""
Utility functions for the transcription system.
"""
import os
from pathlib import Path
from typing import Optional


def get_file_extension(file_path: Path) -> str:
    """Get the file extension in lowercase."""
    return file_path.suffix.lower()


def create_output_filename(input_path: Path, output_dir: Optional[Path] = None) -> Path:
    """Create output filename based on input path."""
    if output_dir is None:
        output_dir = input_path.parent
    
    base_name = input_path.stem
    return output_dir / f"{base_name}_transcription.txt"


def format_timestamp(seconds: float) -> str:
    """Format seconds into HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"


def estimate_processing_time(file_size_mb: float) -> str:
    """Estimate processing time based on file size."""
    # Rough estimate: 1MB ~ 30 seconds processing
    estimated_seconds = file_size_mb * 30
    
    if estimated_seconds < 60:
        return f"~{int(estimated_seconds)} segundos"
    elif estimated_seconds < 3600:
        minutes = int(estimated_seconds / 60)
        return f"~{minutes} minutos"
    else:
        hours = int(estimated_seconds / 3600)
        minutes = int((estimated_seconds % 3600) / 60)
        return f"~{hours}h {minutes}m"


def cleanup_temp_files(*file_paths: Path) -> None:
    """Clean up temporary files."""
    for file_path in file_paths:
        try:
            if file_path.exists():
                file_path.unlink()
        except OSError:
            pass


def validate_file(file_path: Path) -> bool:
    """Validate if file exists and has supported format."""
    if not file_path.exists():
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return False
    
    if not file_path.is_file():
        print(f"Erro: Caminho não é um arquivo: {file_path}")
        return False
    
    supported_extensions = {
        '.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv',  # Video
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'  # Audio
    }
    
    extension = get_file_extension(file_path)
    if extension not in supported_extensions:
        print(f"Erro: Formato não suportado: {extension}")
        print(f"Formatos suportados: {', '.join(sorted(supported_extensions))}")
        return False
    
    return True


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes."""
    return file_path.stat().st_size / (1024 * 1024)


def is_video_file(file_path: Path) -> bool:
    """Check if file is a video file."""
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv'}
    return get_file_extension(file_path) in video_extensions


def ensure_directory_exists(directory: Path) -> None:
    """Ensure directory exists, create if it doesn't."""
    directory.mkdir(parents=True, exist_ok=True)