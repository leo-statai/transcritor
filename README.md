# Audio Transcription System

Minimalist tool to transcribe audio and video files to text using OpenAI Whisper.

## 🚀 Features

- ✅ Multiple video formats (MP4, AVI, MKV, MOV, FLV, WMV)
- ✅ Multiple audio formats (MP3, WAV, FLAC, AAC, OGG, M4A)
- ✅ Automatic audio extraction from video
- ✅ Optional timestamps
- ✅ All Whisper model sizes (tiny, base, small, medium, large)
- ✅ Automatic language detection
- ✅ Simple command-line interface
- ✅ Robust error handling

## 📋 Prerequisites

- Python 3.8+ (tested with Python 3.13)
- FFmpeg installed on the system

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

## 🛠️ Installation

1. **Clone or download the project**
```bash
git clone https://github.com/leo-statai/transcritor.git
cd transcritor
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Basic usage

```bash
# Activate the virtual environment
source venv/bin/activate

# Transcribe a video file
python transcriber.py video.mp4

# Transcribe an audio file
python transcriber.py audio.mp3
```

### Advanced options

```bash
# Custom output file
python transcriber.py video.mp4 -o my_transcript.txt

# Use a larger model (better quality)
python transcriber.py audio.wav --model large

# Force a specific language
python transcriber.py video.mp4 --language pt

# Transcription without timestamps
python transcriber.py audio.mp3 --no-timestamps

# Combine options
python transcriber.py video.mp4 --model medium --language pt -o result.txt
```

### Available options

- `--model`: Whisper model size
  - `tiny`: Fastest, lowest quality (~39M parameters)
  - `base`: Balanced (default) (~74M parameters)
  - `small`: Good quality (~244M parameters)
  - `medium`: High quality (~769M parameters)
  - `large`: Best quality (~1550M parameters)

- `--language`: Language code (e.g. `pt`, `en`, `es`, `fr`)
- `--no-timestamps`: Strip timestamps from the transcript
- `-o, --output`: Output file path

## 📊 Supported formats

### Video
- MP4, AVI, MKV, MOV, FLV, WMV

### Audio
- MP3, WAV, FLAC, AAC, OGG, M4A

## 📄 Output format

The transcript is saved as a TXT file with the following structure:

```
# Audio Transcription
# Model: base
# Language: pt
# Duration: [00:05:30]
#

[00:00:00] Hello, welcome to our podcast.
[00:00:05] Today we're going to talk about technology.
[00:00:10] It's a really interesting topic...
```

## 🧪 Running tests

```bash
# Activate the virtual environment
source venv/bin/activate

# Run tests
python -m unittest tests.test_transcriber -v
```

## ⚡ Performance tips

1. **Model size**: Use `tiny` or `base` for quick tests, `medium` or `large` for maximum quality
2. **Large files**: The system processes audio in chunks automatically to optimize memory
3. **Audio quality**: Clean, clear audio produces better transcripts
4. **Language**: Specifying the language improves accuracy

## ❗ Troubleshooting

### Error: FFmpeg not found
```bash
# Install FFmpeg per the instructions above
which ffmpeg  # Check if installed
```

### Error: Out of memory
- Use a smaller model (`tiny` or `base`)
- Process smaller files
- Close other programs

### Error: Unsupported format
- Confirm the file is in a supported format
- Convert with FFmpeg if needed

### Error: File not found
- Check the file path
- Use absolute paths if needed

## 📁 Project structure

```
transcritor/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI interface
│   ├── audio_extractor.py   # Audio extraction
│   ├── transcriber.py       # Transcription engine
│   └── utils.py             # Helper functions
├── tests/
│   ├── __init__.py
│   └── test_transcriber.py  # Unit tests
├── venv/                    # Virtual environment
├── transcriber.py           # Main entry point
├── requirements.txt         # Dependencies
├── setup.py                 # Package config
├── .gitignore               # Ignored files
└── README.md                # This file
```

## 🤝 Contributing

1. Fork the project
2. Create a branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📝 License

This project is released under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) — transcription engine
- [FFmpeg](https://ffmpeg.org/) — audio/video processing
