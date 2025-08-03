"""
Basic tests for the transcription system.
"""
import unittest
from pathlib import Path
import tempfile
import os

from src.utils import (
    get_file_extension, 
    create_output_filename, 
    format_timestamp,
    validate_file,
    is_video_file,
    get_file_size_mb
)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_get_file_extension(self):
        """Test file extension extraction."""
        self.assertEqual(get_file_extension(Path("test.mp4")), ".mp4")
        self.assertEqual(get_file_extension(Path("test.MP3")), ".mp3")
        self.assertEqual(get_file_extension(Path("file.wav")), ".wav")
    
    def test_create_output_filename(self):
        """Test output filename creation."""
        input_path = Path("/home/user/video.mp4")
        output = create_output_filename(input_path)
        expected = Path("/home/user/video_transcription.txt")
        self.assertEqual(output, expected)
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        self.assertEqual(format_timestamp(0), "[00:00:00]")
        self.assertEqual(format_timestamp(65), "[00:01:05]")
        self.assertEqual(format_timestamp(3665), "[01:01:05]")
    
    def test_is_video_file(self):
        """Test video file detection."""
        self.assertTrue(is_video_file(Path("test.mp4")))
        self.assertTrue(is_video_file(Path("test.avi")))
        self.assertFalse(is_video_file(Path("test.mp3")))
        self.assertFalse(is_video_file(Path("test.wav")))
    
    def test_validate_nonexistent_file(self):
        """Test validation of non-existent file."""
        fake_file = Path("/nonexistent/file.mp4")
        self.assertFalse(validate_file(fake_file))


class TestTranscriber(unittest.TestCase):
    """Test transcriber functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary file for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.temp_file = self.temp_dir / "test.txt"
        self.temp_file.write_text("test content")
    
    def tearDown(self):
        """Clean up test environment."""
        if self.temp_file.exists():
            self.temp_file.unlink()
        if self.temp_dir.exists():
            self.temp_dir.rmdir()
    
    def test_file_size_calculation(self):
        """Test file size calculation."""
        size_mb = get_file_size_mb(self.temp_file)
        self.assertGreater(size_mb, 0)
        self.assertLess(size_mb, 1)  # Should be much less than 1MB


if __name__ == "__main__":
    unittest.main()