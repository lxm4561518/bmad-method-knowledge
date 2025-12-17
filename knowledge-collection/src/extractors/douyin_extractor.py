from .video_extractor import VideoExtractor
from typing import Dict, Optional, Tuple, Any
import os
import yt_dlp
import uuid
import requests
import re
import json

class DouyinExtractor(VideoExtractor):
    def __init__(self, cookies: Optional[Dict[str, str]] = None, model_size: str = "base", cookie_file: Optional[str] = None):
        super().__init__(cookies, model_size)
        self.cookie_file = cookie_file
        # Mobile User-Agent is key for the manual fallback and to bypass desktop WAF
        self.mobile_ua = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

    def _resolve_url_and_get_html(self, url: str) -> Tuple[str, str]:
        headers = {
            'User-Agent': self.mobile_ua,
            'Referer': 'https://www.douyin.com/',
        }
        session = requests.Session()
        # Resolve redirects
        try:
            # We allow redirects to follow short links (v.douyin.com) -> mobile share page
            resp = session.get(url, headers=headers, allow_redirects=True)
            return resp.url, resp.text
        except Exception as e:
            print(f"Failed to resolve URL: {e}")
            return url, ""

    def _extract_manual_info(self, html: str) -> Optional[Dict[str, Any]]:
        """
        Attempts to extract video URL and title from the HTML using regex and JSON parsing.
        This targets the 'window._ROUTER_DATA' object found in mobile/share pages.
        """
        try:
            # Pattern to find the huge JSON data blob
            # We match until the closing script tag or semicolon
            match = re.search(r'window\._ROUTER_DATA\s*=\s*(\{.*?\})(?:;|\s*</script>)', html, re.DOTALL)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                
                # We need to find the video info. It's usually nested deep.
                # Common path: loaderData -> video_(id)/page -> videoInfoRes -> item_list -> [0]
                # We'll search recursively for a dict containing 'video' and 'play_addr'
                
                stack = [data]
                while stack:
                    curr = stack.pop()
                    if isinstance(curr, dict):
                        if 'video' in curr and 'play_addr' in curr['video']:
                            # Found the video object
                            # Double check it has url_list
                            play_addr = curr['video'].get('play_addr', {})
                            url_list = play_addr.get('url_list', [])
                            
                            if url_list:
                                title = curr.get('desc', 'Douyin Video')
                                # Get the first URL
                                final_url = url_list[0]
                                # Hack: replace 'playwm' (watermark) with 'play' (no watermark)
                                # This works for many Douyin CDNs
                                final_url = final_url.replace('playwm', 'play')
                                
                                return {'title': title, 'url': final_url}
                        
                        # Continue searching
                        stack.extend(curr.values())
                    elif isinstance(curr, list):
                        stack.extend(curr)
                        
        except Exception as e:
            print(f"Manual JSON parsing failed: {e}")
        
        return None

    def _download_audio(self, url: str, output_dir: str = "temp_audio") -> Tuple[str, str]:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename_base = str(uuid.uuid4())
        output_template = os.path.join(output_dir, f"{filename_base}.%(ext)s")

        print(f"Starting Douyin extraction for: {url}")

        # 1. Try Manual Extraction First (bypass WAF/Fresh Cookies issue)
        resolved_url, html = self._resolve_url_and_get_html(url)
        manual_info = self._extract_manual_info(html)
        
        target_url = url
        manual_title = None
        
        if manual_info:
            print(f"Manual extraction successful. Title: {manual_info['title']}")
            target_url = manual_info['url']
            manual_title = manual_info['title']
        else:
            print("Manual extraction failed, falling back to yt-dlp native extraction.")
            # If manual failed, use the resolved URL as it might be better than the short one
            target_url = resolved_url

        # 2. Configure yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': False,
            'http_headers': {
                'User-Agent': self.mobile_ua, # Use Mobile UA for download too
                'Referer': 'https://www.douyin.com/',
            }
        }

        # If we have a cookie file, use it. 
        # Even for direct URLs, it doesn't hurt, and for fallback it's required.
        if self.cookie_file and os.path.exists(self.cookie_file):
             ydl_opts['cookiefile'] = self.cookie_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # If manual_info exists, target_url is the direct video file.
                info = ydl.extract_info(target_url, download=True)
                
                # If we have a manual title, prefer it (yt-dlp might not get title from direct file)
                title = manual_title if manual_title else info.get('title', 'Unknown Douyin Video')
                
                filepath = os.path.join(output_dir, f"{filename_base}.mp3")
                return filepath, title
        except Exception as e:
            print(f"Douyin extraction failed: {e}")
            
            error_str = str(e)
            if "Fresh cookies" in error_str:
                 print("\n[SUGGESTION] Even manual fallback failed. Cookies might be totally dead or IP blocked.")
            
            raise e
