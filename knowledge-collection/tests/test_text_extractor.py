import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from extractors.text_extractor import ZhihuExtractor, WeChatExtractor, ToutiaoExtractor

class TestTextExtractors(unittest.TestCase):
    
    @patch('requests.get')
    def test_zhihu_extractor(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <h1 class="QuestionHeader-title">Test Zhihu Title</h1>
            <div class="RichContent-inner">
                <p>This is a test answer.</p>
                <script>console.log('ad');</script>
            </div>
        </html>
        """
        mock_get.return_value = mock_response
        
        extractor = ZhihuExtractor()
        result = extractor.extract("https://www.zhihu.com/question/123")
        
        self.assertEqual(result['title'], "Test Zhihu Title")
        self.assertIn("This is a test answer.", result['content'])
        self.assertNotIn("console.log", result['content'])

    @patch('requests.get')
    def test_wechat_extractor(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <h1 class="rich_media_title">Test WeChat Title</h1>
            <span class="rich_media_meta_text rich_media_meta_nickname">Test Author</span>
            <div class="rich_media_content">
                <p>This is a test article.</p>
            </div>
        </html>
        """
        mock_get.return_value = mock_response
        
        extractor = WeChatExtractor()
        result = extractor.extract("https://mp.weixin.qq.com/s/123")
        
        self.assertEqual(result['title'], "Test WeChat Title")
        self.assertEqual(result['author'], "Test Author")
        self.assertIn("This is a test article.", result['content'])

if __name__ == '__main__':
    unittest.main()
