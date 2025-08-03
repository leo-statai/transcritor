"""
Transcription module using OpenAI Whisper.
"""
import whisper
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm

from utils import format_timestamp, get_file_size_mb, estimate_processing_time


class Transcriber:
    """Handles audio transcription using Whisper."""
    
    def __init__(self, model_size: str = 'base'):
        """
        Initialize transcriber with specified model size.
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model_size = model_size
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load Whisper model."""
        try:
            print(f"Carregando modelo Whisper '{self.model_size}'...")
            self.model = whisper.load_model(self.model_size)
            print("Modelo carregado com sucesso!")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar modelo Whisper: {e}")
    
    def transcribe(
        self, 
        audio_path: Path, 
        language: Optional[str] = None,
        include_timestamps: bool = True
    ) -> Dict:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'pt', 'en'). Auto-detect if None
            include_timestamps: Whether to include timestamps in output
            
        Returns:
            Transcription result dictionary
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")
        
        file_size = get_file_size_mb(audio_path)
        estimated_time = estimate_processing_time(file_size)
        
        print(f"Iniciando transcrição...")
        print(f"Arquivo: {audio_path.name} ({file_size:.1f} MB)")
        print(f"Tempo estimado: {estimated_time}")
        print(f"Modelo: {self.model_size}")
        
        try:
            # Transcribe with progress bar
            options = {
                'language': language,
                'task': 'transcribe',
                'verbose': False
            }
            
            # Remove None values
            options = {k: v for k, v in options.items() if v is not None}
            
            result = self.model.transcribe(str(audio_path), **options)
            
            print("Transcrição concluída!")
            return result
            
        except Exception as e:
            raise RuntimeError(f"Erro durante transcrição: {e}")
    
    def format_output(self, result: Dict, include_timestamps: bool = True) -> str:
        """
        Format transcription result for output.
        
        Args:
            result: Whisper transcription result
            include_timestamps: Whether to include timestamps
            
        Returns:
            Formatted transcription text
        """
        if not result.get('segments'):
            return result.get('text', '').strip()
        
        formatted_lines = []
        
        if include_timestamps:
            for segment in result['segments']:
                timestamp = format_timestamp(segment['start'])
                text = segment['text'].strip()
                if text:
                    formatted_lines.append(f"{timestamp} {text}")
        else:
            # Combine all text without timestamps
            text = result.get('text', '').strip()
            formatted_lines.append(text)
        
        return '\n'.join(formatted_lines)
    
    def save_transcription(
        self, 
        result: Dict, 
        output_path: Path,
        include_timestamps: bool = True
    ) -> None:
        """
        Save transcription to file.
        
        Args:
            result: Whisper transcription result
            output_path: Path to save transcription
            include_timestamps: Whether to include timestamps
        """
        formatted_text = self.format_output(result, include_timestamps)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Add header with metadata
                f.write(f"# Transcrição de Áudio\n")
                f.write(f"# Modelo: {self.model_size}\n")
                f.write(f"# Idioma: {result.get('language', 'auto-detectado')}\n")
                f.write(f"# Duração: {format_timestamp(len(result.get('segments', [])) * 30)}\n")
                f.write(f"#\n\n")
                
                f.write(formatted_text)
                
                if not formatted_text.endswith('\n'):
                    f.write('\n')
            
            print(f"Transcrição salva em: {output_path}")
            
        except Exception as e:
            raise RuntimeError(f"Erro ao salvar transcrição: {e}")
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model."""
        return {
            'model_size': self.model_size,
            'parameters': {
                'tiny': '39M',
                'base': '74M', 
                'small': '244M',
                'medium': '769M',
                'large': '1550M'
            }.get(self.model_size, 'Unknown')
        }