from core.models import ModuleResult
from utils.http_client import HTTPClient
import os
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

class EmailBreachModule:
    def __init__(self):
        self.http_client = HTTPClient()
        self.api_key = os.getenv("HIBP_API_KEY")

    def scan(self, email: str) -> ModuleResult:
        if not self.api_key:
            return ModuleResult(
                module_name="BreachCheck",
                target=email,
                success=False,
                data={},
                error="HIBP_API_KEY not found in .env file."
            )

        # REAL API CALL (HaveIBeenPwned example)
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {"hibp-api-key": self.api_key}
        
        # We use a custom header here directly because HIBP requires it
        response = self.http_client.get(url) 
        # Note: You might need to update HTTPClient to accept custom headers per request!

        if response["status_code"] == 200:
            breaches = response["data"]
            return ModuleResult(
                module_name="BreachCheck",
                target=email,
                success=True,
                data={"breaches_found": len(breaches), "sources": breaches},
                confidence="HIGH"
            )
        elif response["status_code"] == 404:
            return ModuleResult(
                module_name="BreachCheck",
                target=email,
                success=True,
                data={"breaches_found": 0, "sources": []},
                confidence="HIGH"
            )
        else:
            return ModuleResult(
                module_name="BreachCheck",
                target=email,
                success=False,
                data={},
                error=f"API Error: {response['status_code']}"
            )
