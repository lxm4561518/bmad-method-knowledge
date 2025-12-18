import argparse
import json
import os
import sys
import re
from datetime import datetime
from extractors.factory import ExtractorFactory
from cookie_manager import CookieManager

def sanitize_filename(name):
    """Sanitize string to be used as a filename."""
    # Remove invalid characters for Windows/Linux filesystems
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Replace whitespace with underscores or keep as spaces (user preference usually spaces or simple)
    # Let's keep spaces but strip leading/trailing
    return name.strip()

def main():
    parser = argparse.ArgumentParser(description="Knowledge Collection CLI")
    parser.add_argument("url", help="Target URL to extract content from")
    parser.add_argument("--cookie-source", default="cookies", help="Path to cookies directory or cookies.json file")
    parser.add_argument("--output-dir", default="outputs", help="Directory to save output JSON")
    parser.add_argument("--model-size", default="base", choices=["tiny", "base", "small", "medium", "large", "large-v3"], help="Whisper model size (default: base)")
    
    args = parser.parse_args()
    
    # 1. Init Cookie Manager
    # Resolve absolute path if needed, but relative to cwd is fine for CLI
    cookie_manager = CookieManager(args.cookie_source)
    
    # 2. Determine domain for cookies (simple heuristic)
    domain_key = "default"
    if "zhihu.com" in args.url: domain_key = "zhihu"
    elif "weixin.qq.com" in args.url: domain_key = "wechat"
    elif "toutiao.com" in args.url: domain_key = "toutiao"
    elif "bilibili.com" in args.url: domain_key = "bilibili"
    elif "douyin.com" in args.url: domain_key = "douyin"
    
    cookies = cookie_manager.get_cookies_for_domain(domain_key)
    cookie_file = cookie_manager.get_cookie_file_for_domain(domain_key)
    if cookies:
        print(f"Loaded cookies for domain: {domain_key}")
    if cookie_file:
        print(f"Using cookie file: {cookie_file}")
    
    # 3. Get Extractor
    extractor = ExtractorFactory.get_extractor(args.url, cookies, cookie_file, model_size=args.model_size)
    if not extractor:
        print(f"Error: No suitable extractor found for URL: {args.url}")
        sys.exit(1)
        
    try:
        print(f"Extracting content from: {args.url}")
        result = extractor.extract(args.url)
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        
        # 4. Save Output
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
            
        # Create a safe filename from title or domain + timestamp
        title = result.get('title')
        if title:
            safe_title = sanitize_filename(title)
            # Ensure filename isn't too long (Windows max path is 260, but filename limit is usually 255)
            if len(safe_title) > 200:
                safe_title = safe_title[:200]
            filename = f"{safe_title}.json"
        else:
            filename = f"{domain_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        filepath = os.path.join(args.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"Success! Output saved to: {filepath}")
        
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
