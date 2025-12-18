from .base import BaseExtractor
from typing import Dict, Any, Optional, Tuple
import os
import yt_dlp
import whisper
import uuid

class VideoExtractor(BaseExtractor):
    def __init__(self, cookies: Optional[Dict[str, str]] = None, model_size: str = "base"):
        super().__init__(cookies)
        self.model_size = model_size
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"Loading Whisper model: {self.model_size}...")
            self._model = whisper.load_model(self.model_size)
        return self._model

    def _download_audio(self, url: str, output_dir: str = "temp_audio") -> Tuple[str, str]:
        """
        Downloads audio from URL using yt-dlp.
        Returns (audio_filepath, title).
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename_base = str(uuid.uuid4())
        output_template = os.path.join(output_dir, f"{filename_base}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Referer': 'https://www.bilibili.com/',
            }
        }

        # Inject cookies if available
        if self.cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
            ydl_opts['http_headers']['Cookie'] = cookie_str

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown Video')
            # The actual filename might have the extension appended
            filepath = os.path.join(output_dir, f"{filename_base}.mp3")
            return filepath, title

    def _transcribe_audio(self, filepath: str) -> str:
        """
        Transcribes audio file using Whisper.
        Uses initial_prompt to encourage punctuation and segments for better readability.
        """
        print(f"Transcribing {filepath}...")
        # Use initial_prompt to guide the model to use punctuation
        result = self.model.transcribe(
            filepath, 
            language='zh',
            initial_prompt="这是一段中文对话，包括标点符号。"
        )
        
        # Prefer segments with newlines for better readability
        if 'segments' in result and result['segments']:
            text_segments = [seg['text'].strip() for seg in result['segments']]
            return "\n".join(text_segments)
            
        return result['text']

    def extract(self, url: str) -> Dict[str, Any]:
        audio_path = None
        try:
            # 1. Download
            print(f"Downloading audio from {url}...")
            audio_path, title = self._download_audio(url)
            
            # 2. Transcribe
            content = self._transcribe_audio(audio_path)
            
            # 3. Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
            return {
                "title": title.strip(),
                "content": content.strip(),
                "url": url
            }
            
        except Exception as e:
            # Cleanup on error
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            raise e
