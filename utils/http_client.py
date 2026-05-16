import requests
from typing import Optional, Dict, Any

class HTTPClient:
    """
    A unified wrapper for all network requests. 
    Centralizing this allows you to add security features globally.
    """
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.default_headers = {
            "User-Agent": "AutoOSINT/1.0 (Security Research Tool; +https://github.com/yourusername/AutoOSINT)"
        }

    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform a safe GET request and return a standardized response.
        """
        # Merge default headers with request-specific headers
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = requests.get(
                url, 
                params=params, 
                headers=request_headers, 
                timeout=self.timeout
            )
            
            # Handle potential JSON decoding errors
            try:
                data = response.json()
            except ValueError:
                data = response.text

            return {
                "status_code": response.status_code,
                "data": data,
                "error": None if response.status_code < 400 else f"HTTP Error {response.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": None,
                "error": str(e)
            }

    def post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Dict[str, Any]:
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = requests.post(
                url, 
                json=data, 
                headers=request_headers, 
                timeout=self.timeout
            )
            return {
                "status_code": response.status_code,
                "data": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text,
                "error": None if response.status_code < 200 else f"HTTP Error {response.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": None,
                "error": str(e)
            }
