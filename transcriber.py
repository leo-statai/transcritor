#!/usr/bin/env python3
"""
Entry point script for the audio transcription system.
This allows users to run the transcriber directly with 'python transcriber.py'
"""
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import main

if __name__ == "__main__":
    main()