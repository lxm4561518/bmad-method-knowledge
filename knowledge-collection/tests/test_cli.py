import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import main

class TestCLI(unittest.TestCase):
    
    @patch('main.ExtractorFactory')
    @patch('main.CookieManager')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_main_success_flow(self, mock_json_dump, mock_open, mock_makedirs, mock_print, mock_parse_args, mock_cookie_cls, mock_factory_cls):
        # Setup mocks
        mock_args = MagicMock()
        mock_args.url = "https://www.zhihu.com/question/123"
        mock_args.cookie_file = "cookies.json"
        mock_args.output_dir = "outputs"
        mock_parse_args.return_value = mock_args
        
        mock_cookie_instance = MagicMock()
        mock_cookie_instance.get_cookies_for_domain.return_value = {'key': 'value'}
        mock_cookie_cls.return_value = mock_cookie_instance
        
        mock_extractor = MagicMock()
        mock_extractor.extract.return_value = {'title': 'Test', 'content': 'Content'}
        mock_factory_cls.get_extractor.return_value = mock_extractor
        
        # Run main
        main()
        
        # Assertions
        mock_cookie_cls.assert_called_with("cookies.json")
        mock_cookie_instance.get_cookies_for_domain.assert_called_with("zhihu")
        mock_factory_cls.get_extractor.assert_called()
        mock_extractor.extract.assert_called_with("https://www.zhihu.com/question/123")
        mock_json_dump.assert_called()

    @patch('main.ExtractorFactory')
    @patch('main.CookieManager') # Add missing patch for CookieManager init
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_extractor(self, mock_exit, mock_parse_args, mock_cookie_cls, mock_factory_cls):
        mock_args = MagicMock()
        mock_args.url = "https://unknown.com"
        mock_args.cookie_file = "cookies.json"
        mock_args.output_dir = "outputs"
        mock_parse_args.return_value = mock_args
        
        mock_factory_cls.get_extractor.return_value = None
        
        main()
        
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
