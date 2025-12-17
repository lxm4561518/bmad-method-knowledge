import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from extractors.video_extractor import VideoExtractor

class TestVideoExtractor(unittest.TestCase):

    @patch('yt_dlp.YoutubeDL')
    @patch('whisper.load_model')
    @patch('os.path.exists')
    @patch('os.remove')
    @patch('os.makedirs')
    def test_extract_flow(self, mock_makedirs, mock_remove, mock_exists, mock_load_model, mock_ydl):
        # Mock Whisper model
        mock_model_instance = MagicMock()
        mock_model_instance.transcribe.return_value = {'text': 'Transcribed text content'}
        mock_load_model.return_value = mock_model_instance

        # Mock yt-dlp
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.return_value = {'title': 'Test Video Title'}
        mock_ydl.return_value.__enter__.return_value = mock_ydl_instance

        extractor = VideoExtractor()
        
        # We need to mock _download_audio return because it does file operations we want to avoid in unit test
        # But here we are testing the full flow including the _download_audio logic (with mocked ydl)
        # The file path returned by _download_audio is constructed inside it.
        # We can just let it run since we mocked ydl.extract_info and os.makedirs.
        
        # However, _download_audio returns a path that doesn't exist. 
        # _transcribe_audio calls model.transcribe(filepath). 
        # Since we mocked the model instance, it won't actually try to open the file.
        
        result = extractor.extract("https://www.bilibili.com/video/BV123")
        
        self.assertEqual(result['title'], "Test Video Title")
        self.assertEqual(result['content'], "Transcribed text content")
        
        # Verify calls
        mock_ydl_instance.extract_info.assert_called_with("https://www.bilibili.com/video/BV123", download=True)
        mock_model_instance.transcribe.assert_called()
        mock_remove.assert_called() # Cleanup should happen

if __name__ == '__main__':
    unittest.main()
