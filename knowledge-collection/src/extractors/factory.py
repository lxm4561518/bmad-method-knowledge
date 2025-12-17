from typing import Optional, Dict
from .base import BaseExtractor
from .text_extractor import ZhihuExtractor, WeChatExtractor, ToutiaoExtractor
from .video_extractor import VideoExtractor

class ExtractorFactory:
    @staticmethod
    def get_extractor(url: str, cookies: Optional[Dict[str, str]] = None) -> Optional[BaseExtractor]:
        if "zhihu.com" in url:
            return ZhihuExtractor(cookies)
        elif "weixin.qq.com" in url:
            return WeChatExtractor(cookies)
        elif "toutiao.com" in url:
            return ToutiaoExtractor(cookies)
        elif "bilibili.com" in url or "douyin.com" in url:
            return VideoExtractor(cookies)
        else:
            return None
