import json
import os
import glob
from http.cookiejar import MozillaCookieJar
from typing import Dict, Optional

class CookieManager:
    def __init__(self, cookie_source: str = "cookies"):
        """
        Args:
            cookie_source: Path to a directory containing .txt cookie files (Netscape format),
                           or path to a .json file (legacy support).
        """
        self.cookie_source = cookie_source
        self.cookies = {}
        self._load_cookies()

    def _load_cookies(self):
        if os.path.isdir(self.cookie_source):
            self._load_from_directory()
        elif os.path.isfile(self.cookie_source) and self.cookie_source.endswith('.json'):
            self._load_from_json()
        else:
            # If it's a file but not json, maybe it's a single netscape file? 
            # For now, let's stick to dir or json.
            pass

    def _load_from_directory(self):
        """Loads all .txt files in the directory as Netscape cookies."""
        txt_files = glob.glob(os.path.join(self.cookie_source, "*.txt"))
        for filepath in txt_files:
            filename = os.path.basename(filepath)
            domain_key = os.path.splitext(filename)[0] # e.g., 'zhihu' from 'zhihu.txt'
            
            try:
                cj = MozillaCookieJar(filepath)
                cj.load(ignore_discard=True, ignore_expires=True)
                
                # Convert to dict for requests
                cookie_dict = {}
                for cookie in cj:
                    cookie_dict[cookie.name] = cookie.value
                
                self.cookies[domain_key] = cookie_dict
                # print(f"Loaded cookies for {domain_key} from {filename}")
            except Exception as e:
                print(f"Warning: Failed to load cookies from {filepath}: {e}")

    def _load_from_json(self):
        """Legacy support for single JSON file."""
        try:
            with open(self.cookie_source, 'r', encoding='utf-8') as f:
                self.cookies = json.load(f)
        except Exception as e:
            print(f"Warning: Error loading cookies from {self.cookie_source}: {e}")

    def get_cookies_for_domain(self, domain_key: str) -> Dict[str, str]:
        """
        Returns cookies for a given domain key (e.g., 'zhihu', 'wechat', 'bilibili').
        """
        return self.cookies.get(domain_key, {})
