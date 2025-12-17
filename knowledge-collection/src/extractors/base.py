from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class BaseExtractor(ABC):
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        self.cookies = cookies or {}

    @abstractmethod
    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract content from the given URL.
        Returns a dictionary with structured data.
        """
        pass
