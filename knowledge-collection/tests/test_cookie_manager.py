import unittest
import os
import shutil
import tempfile
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cookie_manager import CookieManager

class TestCookieManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        
    def test_load_from_directory(self):
        # Create a dummy netscape cookie file
        zhihu_cookie_content = """# Netscape HTTP Cookie File
.zhihu.com	TRUE	/	FALSE	1799980255	_xsrf	test_xsrf_value
"""
        with open(os.path.join(self.test_dir, "zhihu.txt"), "w") as f:
            f.write(zhihu_cookie_content)
            
        manager = CookieManager(self.test_dir)
        
        cookies = manager.get_cookies_for_domain("zhihu")
        self.assertEqual(cookies.get("_xsrf"), "test_xsrf_value")
        
    def test_load_nonexistent_dir(self):
        manager = CookieManager("nonexistent_dir")
        self.assertEqual(manager.cookies, {})

if __name__ == '__main__':
    unittest.main()
