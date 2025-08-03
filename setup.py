from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="audio-transcriber",
    version="1.0.0",
    author="Audio Transcriber Team",
    description="Sistema minimalista de transcrição de áudio usando Whisper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai-whisper==20231117",
        "ffmpeg-python==0.2.0",
        "tqdm==4.66.1",
    ],
    entry_points={
        "console_scripts": [
            "transcriber=src.main:main",
        ],
    },
)