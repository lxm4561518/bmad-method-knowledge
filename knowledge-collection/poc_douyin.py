import yt_dlp
import os
import sys

# Ensure we are in the right directory or handle paths correctly
# This script assumes it's run from knowledge-collection/ or we adjust paths

def test_douyin():
    url = "https://v.douyin.com/WopqOr75-OM/"
    
    # Try to find the cookie file relative to this script or current cwd
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = os.path.join(base_dir, "cookies", "douyin.txt")
    
    if not os.path.exists(cookie_file):
        print(f"Cookie file not found at: {cookie_file}")
        # Try relative to cwd
        cookie_file = os.path.abspath("cookies/douyin.txt")
        if not os.path.exists(cookie_file):
             print(f"Cookie file not found at: {cookie_file}")
             return

    print(f"Testing Douyin extraction with cookie file: {cookie_file}")
    
    ydl_opts = {
        'cookiefile': cookie_file, # Pass file path directly
        'quiet': False,
        'no_warnings': False,
        # 'verbose': True, # Enable for debugging
        'format': 'bestaudio/best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
            'Referer': 'https://www.douyin.com/',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False) # Just extract info for POC
            print("Extraction successful!")
            print(f"Title: {info.get('title')}")
            print(f"ID: {info.get('id')}")
    except Exception as e:
        print(f"Extraction failed: {e}")

if __name__ == "__main__":
    test_douyin()
