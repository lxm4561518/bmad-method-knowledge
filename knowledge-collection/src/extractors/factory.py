from typing import Optional, Dict
from .base import BaseExtractor
from .text_extractor import ZhihuExtractor, WeChatExtractor, ToutiaoExtractor
from .video_extractor import VideoExtractor
from .douyin_extractor import DouyinExtractor

class ExtractorFactory:
    @staticmethod
    def get_extractor(url: str, cookies: Optional[Dict[str, str]] = None, cookie_file: Optional[str] = None) -> Optional[BaseExtractor]:
        if "zhihu.com" in url:
            return ZhihuExtractor(cookies)
        elif "weixin.qq.com" in url:
            return WeChatExtractor(cookies)
        elif "toutiao.com" in url:
            return ToutiaoExtractor(cookies)
        elif "douyin.com" in url:
            return DouyinExtractor(cookies, cookie_file=cookie_file)
        elif "bilibili.com" in url:
            return VideoExtractor(cookies)
        else:
            return None
