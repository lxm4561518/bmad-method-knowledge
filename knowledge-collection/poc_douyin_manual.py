import requests
import re
import json
import yt_dlp
import os

def test_manual_douyin():
    url = "https://v.douyin.com/WopqOr75-OM/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
    }
    
    print(f"1. Resolving URL: {url}")
    session = requests.Session()
    # Load cookies?
    cookie_file = os.path.abspath("cookies/douyin.txt")
    if os.path.exists(cookie_file):
        # Very basic cookie parser for requests
        with open(cookie_file, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip(): continue
                parts = line.split('\t')
                if len(parts) >= 7:
                    session.cookies.set(parts[5], parts[6], domain=parts[0])

    try:
        resp = session.get(url, headers=headers, allow_redirects=True)
        print(f"Final URL: {resp.url}")
        
        # Search for video patterns
        # Look for the video ID
        video_id = ""
        match = re.search(r'video/(\d+)', resp.url)
        if match:
            video_id = match.group(1)
            print(f"Found Video ID: {video_id}")
        
        # 2. Get HTML Content
        print("Fetching HTML content...")
        # Ensure we use the same session and headers
        resp = session.get(resp.url, headers=headers)
        html = resp.text
        print(f"HTML Length: {len(html)}")
        
        # Save HTML for inspection
        with open("debug_douyin.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML to debug_douyin.html")

        video_url = None
        
        # Pattern 1: Render Data (URL encoded)
        render_data_match = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', html)
        if render_data_match:
            print("Found RENDER_DATA")
            try:
                raw_data = render_data_match.group(1)
                from urllib.parse import unquote
                decoded_data = unquote(raw_data)
                data = json.loads(decoded_data)
                
                # Traverse: app -> videoDetail -> video -> playAddr -> urlList -> [0]
                # Note: Structure changes often.
                # Let's try to dump the keys or search in the decoded string
                
                # Quick hack: search in decoded string
                url_match = re.search(r'"play_addr":\{.*?"url_list":\["(.*?)"', decoded_data)
                if url_match:
                    video_url = url_match.group(1).replace(r'\/', '/')
                    print(f"Found URL in RENDER_DATA: {video_url}")
            except Exception as e:
                print(f"Error parsing RENDER_DATA: {e}")

        # Pattern 2: Raw Regex in HTML
        if not video_url:
            # "url_list":["https://..."]
            # Look for aweme/v1/play
            url_match = re.search(r'"url_list":\["(https://www\.iesdouyin\.com/aweme/v1/play/.*?)"', html)
            if url_match:
                 video_url = url_match.group(1).replace(r'\/', '/')
                 print(f"Found URL via Regex 2: {video_url}")
        
        if video_url:
            print("-" * 20)
            print(f"Attempting yt-dlp on DIRECT VIDEO URL: {video_url}")
            
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'http_headers': headers,
                # 'cookiefile': cookie_file if os.path.exists(cookie_file) else None # Direct URL might not need cookies if we have the token in URL
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(video_url, download=False)
        else:
            print("Could not find video URL in HTML.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_manual_douyin()
