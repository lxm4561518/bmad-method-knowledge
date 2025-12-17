import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extractors.douyin_extractor import DouyinExtractor

def test():
    url = "https://v.douyin.com/WopqOr75-OM/"
    # Point to the cookie file if it exists
    cookie_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "cookies", "douyin.txt"))
    
    print(f"Cookie file path: {cookie_file}")
    
    extractor = DouyinExtractor(cookie_file=cookie_file)
    try:
        print(f"Testing extraction for: {url}")
        result = extractor.extract(url)
        print("SUCCESS!")
        print(f"Title: {result.get('title')}")
        # print(f"Content: {result.get('content')[:100]}...")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
