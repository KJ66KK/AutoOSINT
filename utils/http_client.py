import requests
from typing import Optional, Dict, Any

class HTTPClient:
    """
    A unified wrapper for all network requests. 
    Centralizing this allows you to add security features globally.
    """
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        # PRO TIP: 
        # 1. Use 'requests.Session()' here to keep connections alive (faster).
        # 2. To avoid being blocked, rotate your 'User-Agent' from a list of common browsers.
        # 3. Add a 'self.proxies' dict if you want to route traffic through Tor or VPNs.
        self.headers = {
            "User-Agent": "AutoOSINT/1.0 (Security Research Tool; +https://github.com/yourusername/AutoOSINT)"
        }

    def get(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform a safe GET request and return a standardized response.
        """
        try:
            response = requests.get(
                url, 
                params=params, 
                headers=self.headers, 
                timeout=self.timeout
            )
            return {
                "status_code": response.status_code,
                "data": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text,
                "error": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": None,
                "error": str(e)
            }

    def post(self, url: str, data: Dict) -> Dict[str, Any]:
        """
        Perform a safe POST request.
        """
        try:
            response = requests.post(
                url, 
                json=data, 
                headers=self.headers, 
                timeout=self.timeout
            )
            return {
                "status_code": response.status_code,
                "data": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text,
                "error": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": None,
                "error": str(e)
            }
