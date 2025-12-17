from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
import sys

# Add current directory to sys.path to ensure imports work if run from src/ or parent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extractors.factory import ExtractorFactory
from cookie_manager import CookieManager

app = FastAPI(title="Content Extractor API")

# Initialize CookieManager
# Assuming cookies directory is relative to the execution context or fixed path
# We'll try to find 'cookies' dir in parent or current dir
COOKIE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cookies")
if not os.path.exists(COOKIE_DIR):
    COOKIE_DIR = "cookies" # Fallback to current working directory

cookie_manager = CookieManager(COOKIE_DIR)

class ExtractRequest(BaseModel):
    url: str

class ExtractResponse(BaseModel):
    title: str
    content: str
    url: str
    timestamp: str

def get_domain_key(url: str) -> str:
    if "zhihu.com" in url: return "zhihu"
    elif "weixin.qq.com" in url: return "wechat"
    elif "toutiao.com" in url: return "toutiao"
    elif "bilibili.com" in url: return "bilibili"
    elif "douyin.com" in url: return "douyin"
    return "default"

@app.post("/extract", response_model=ExtractResponse)
async def extract_content(request: ExtractRequest):
    url = request.url
    domain_key = get_domain_key(url)
    
    # Reload cookies might be expensive per request, but ensures freshness. 
    # For now, we use the pre-loaded manager or rely on manager internal logic.
    # The current CookieManager loads on init. We might want to reload if needed, 
    # but let's stick to simple implementation first.
    cookies = cookie_manager.get_cookies_for_domain(domain_key)
    
    extractor = ExtractorFactory.get_extractor(url, cookies)
    if not extractor:
        raise HTTPException(status_code=400, detail=f"No suitable extractor found for URL: {url}")
    
    try:
        # Note: extractor.extract might be blocking (especially video).
        # In a real production app, we should run this in a thread pool or make extractors async.
        # FastAPI handles normal def functions in a thread pool, so this is okay for MVP.
        result = extractor.extract(url)
        
        return ExtractResponse(
            title=result.get("title", "No Title"),
            content=result.get("content", ""),
            url=result.get("url", url),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
