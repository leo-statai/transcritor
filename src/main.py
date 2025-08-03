#!/usr/bin/env python3
"""
Main CLI interface for the audio transcription system.
"""
import argparse
import sys
from pathlib import Path

from audio_extractor import AudioExtractor
from transcriber import Transcriber
from utils import validate_file, create_output_filename, get_file_size_mb


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Transcrever arquivos de áudio e vídeo para texto usando Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s video.mp4
  %(prog)s audio.mp3 -o transcricao.txt
  %(prog)s video.mp4 --model large --language pt
  %(prog)s audio.wav --no-timestamps
        """
    )
    
    parser.add_argument(
        'input',
        type=Path,
        help='Arquivo de entrada (vídeo ou áudio)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Arquivo de saída (padrão: <nome_entrada>_transcription.txt)'
    )
    
    parser.add_argument(
        '--model',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='base',
        help='Tamanho do modelo Whisper (padrão: base)'
    )
    
    parser.add_argument(
        '--language',
        help='Idioma do áudio (ex: pt, en, es). Auto-detectado se não especificado'
    )
    
    parser.add_argument(
        '--no-timestamps',
        action='store_true',
        help='Não incluir timestamps na transcrição'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Audio Transcriber 1.0.0'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Validate input file
    if not validate_file(args.input):
        sys.exit(1)
    
    # Create output path if not specified
    output_path = args.output or create_output_filename(args.input)
    
    # Initialize components
    extractor = AudioExtractor()
    transcriber = None
    
    try:
        print("=== Sistema de Transcrição de Áudio ===")
        print(f"Arquivo de entrada: {args.input}")
        print(f"Arquivo de saída: {output_path}")
        print(f"Modelo Whisper: {args.model}")
        print()
        
        # Process audio extraction
        print("Fase 1: Processamento de áudio")
        audio_path = extractor.process(args.input)
        
        if audio_path != args.input:
            print(f"Áudio extraído para: {audio_path}")
        else:
            print("Usando arquivo de áudio original")
        
        print()
        
        # Initialize transcriber
        print("Fase 2: Carregamento do modelo")
        transcriber = Transcriber(model_size=args.model)
        
        # Show model info
        model_info = transcriber.get_model_info()
        print(f"Modelo carregado: {model_info['model_size']} ({model_info['parameters']} parâmetros)")
        print()
        
        # Transcribe audio
        print("Fase 3: Transcrição")
        result = transcriber.transcribe(
            audio_path,
            language=args.language,
            include_timestamps=not args.no_timestamps
        )
        
        print()
        
        # Save transcription
        print("Fase 4: Salvando resultado")
        transcriber.save_transcription(
            result,
            output_path,
            include_timestamps=not args.no_timestamps
        )
        
        # Show statistics
        print()
        print("=== Estatísticas ===")
        if result.get('segments'):
            print(f"Segmentos processados: {len(result['segments'])}")
        
        if result.get('language'):
            print(f"Idioma detectado: {result['language']}")
        
        file_size = get_file_size_mb(args.input)
        print(f"Tamanho do arquivo: {file_size:.1f} MB")
        
        print()
        print("✓ Transcrição concluída com sucesso!")
        
    except KeyboardInterrupt:
        print("\n\nTranscrição interrompida pelo usuário.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nErro: {e}", file=sys.stderr)
        sys.exit(1)
        
    finally:
        # Cleanup temporary files
        if extractor:
            extractor.cleanup()


if __name__ == "__main__":
    main()