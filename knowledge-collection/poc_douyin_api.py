import requests
import json
import yt_dlp
import os

def test_api():
    video_id = "7582914250524413219"
    resolved_url = "https://www.iesdouyin.com/share/video/7582914250524413219/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.douyin.com/',
        'Cookie': 's_v_web_id=verify_layvk80b_o1lGd5sE_9pQ0_4s8A_8tqR_5qS8tqR5qS8t' # Sometimes a dummy cookie helps
    }

    print("--- Test 1: Public API (v2 iteminfo) ---")
    api_url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
    try:
        resp = requests.get(api_url, headers=headers)
        print(f"API Status: {resp.status_code}")
        data = resp.json()
        # print(json.dumps(data, indent=2))
        
        if data.get('item_list'):
            vid_url = data['item_list'][0]['video']['play_addr']['url_list'][0]
            print(f"FOUND VIDEO URL (API): {vid_url}")
            # The URL usually has 'playwm' (watermark). Replace with 'play' for no-watermark?
            # Douyin URLs are often like: https://aweme.snssdk.com/aweme/v1/playwm/?video_id=...
            # To get no watermark, change 'playwm' to 'play'
            no_wm_url = vid_url.replace('playwm', 'play')
            print(f"No-Watermark URL: {no_wm_url}")
            return no_wm_url
        else:
            print("API returned no item_list. (Might be deprecated or blocked)")
            
    except Exception as e:
        print(f"API Test Failed: {e}")

    print("\n--- Test 2: yt-dlp on Resolved URL ---")
    # Sometimes passing the final mobile URL to yt-dlp works better than the short link
    ydl_opts = {
        'quiet': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(resolved_url, download=False)
    except Exception as e:
        print(f"yt-dlp on resolved URL failed: {e}")

if __name__ == "__main__":
    test_api()
