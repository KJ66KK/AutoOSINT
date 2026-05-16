from core.models import ModuleResult
from utils.http_client import HTTPClient
import os
from dotenv import load_dotenv

load_dotenv()

class EmailBreachModule:
    """
    Email Breach Check using LeakCheck.io (Free Tier Friendly).
    """
    def __init__(self):
        self.http_client = HTTPClient()
        self.api_key = os.getenv("LEAKCHECK_API_KEY")

    def scan(self, email: str) -> ModuleResult:
        # If no key, we can still use their public free endpoint (if available) 
        # or report error.
        if not self.api_key:
            return ModuleResult(
                module_name="BreachCheck",
                target=email,
                success=False,
                data={},
                error="LEAKCHECK_API_KEY not found in .env file."
            )

        # LeakCheck.io API v2
        url = f"https://leakcheck.io/api/v2/query/{email}"
        params = {"key": self.api_key, "type": "email"}
        
        response = self.http_client.get(url, params=params)

        if response["status_code"] == 200 and isinstance(response["data"], dict):
            api_data = response["data"]
            if api_data.get("success"):
                sources = [item.get("source") for sublist in api_data.get("sources", []) for item in sublist] if isinstance(api_data.get("sources"), list) else []
                return ModuleResult(
                    module_name="BreachCheck",
                    target=email,
                    success=True,
                    data={
                        "breach_found": api_data.get("found", 0) > 0,
                        "total_leaks": api_data.get("found", 0),
                        "sources": api_data.get("sources", [])
                    },
                    confidence="HIGH"
                )
            else:
                return ModuleResult(
                    module_name="BreachCheck",
                    target=email,
                    success=False,
                    data={},
                    error=f"LeakCheck API: {api_data.get('error', 'Unknown error')}"
                )
        
        return ModuleResult(
            module_name="BreachCheck",
            target=email,
            success=False,
            data={},
            error=f"HTTP Error: {response['status_code']}"
        )
