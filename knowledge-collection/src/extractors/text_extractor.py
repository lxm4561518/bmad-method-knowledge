from .base import BaseExtractor
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
import re


class TextExtractor(BaseExtractor):
    def _get_soup(self, url: str) -> BeautifulSoup:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, cookies=self.cookies)
        response.encoding = 'utf-8' # Force utf-8
        return BeautifulSoup(response.text, 'html.parser')

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        return text.strip()

    def extract(self, url: str) -> Dict[str, Any]:
        # Default implementation (fallback)
        soup = self._get_soup(url)
        title = soup.title.string if soup.title else "No Title"
        content = soup.get_text()
        return {
            "title": self._clean_text(title), 
            "content": self._clean_text(content), 
            "url": url
        }

class ZhihuExtractor(TextExtractor):
    def extract(self, url: str) -> Dict[str, Any]:
        soup = self._get_soup(url)
        
        # Try to find question title
        title_tag = soup.find('h1', class_='QuestionHeader-title')
        if not title_tag:
            title_tag = soup.find('h1', class_='Post-Title') # For articles
            
        title = title_tag.get_text() if title_tag else "Zhihu Content"
        
        # Try to find content
        # This is a simplified logic. Real Zhihu pages are complex.
        content_tag = soup.find('div', class_='RichContent-inner')
        if not content_tag:
             content_tag = soup.find('div', class_='Post-RichText') # For articles

        content = ""
        if content_tag:
            # Remove style tags and scripts
            for script in content_tag(["script", "style"]):
                script.extract()
            content = content_tag.get_text(separator='\n')
        
        return {
            "title": self._clean_text(title),
            "content": self._clean_text(content),
            "url": url
        }

class WeChatExtractor(TextExtractor):
    def extract(self, url: str) -> Dict[str, Any]:
        soup = self._get_soup(url)
        
        title_tag = soup.find('h1', class_='rich_media_title')
        title = title_tag.get_text() if title_tag else "WeChat Article"
        
        # Meta info
        author_tag = soup.find('span', class_='rich_media_meta_text rich_media_meta_nickname')
        author = author_tag.get_text() if author_tag else "Unknown"
        
        content_tag = soup.find('div', class_='rich_media_content')
        content = ""
        if content_tag:
            for script in content_tag(["script", "style"]):
                script.extract()
            content = content_tag.get_text(separator='\n')
            
        return {
            "title": self._clean_text(title),
            "author": self._clean_text(author),
            "content": self._clean_text(content),
            "url": url
        }

class ToutiaoExtractor(TextExtractor):
    def extract(self, url: str) -> Dict[str, Any]:
        soup = self._get_soup(url)
        
        title_tag = soup.find('h1', class_='article-title')
        title = title_tag.get_text() if title_tag else "Toutiao Article"
        
        content_tag = soup.find('div', class_='article-content')
        content = ""
        if content_tag:
            for script in content_tag(["script", "style"]):
                script.extract()
            content = content_tag.get_text(separator='\n')
            
        return {
            "title": self._clean_text(title),
            "content": self._clean_text(content),
            "url": url
        }
