from core.models import ModuleResult
from utils.http_client import HTTPClient
import phonenumbers
from phonenumbers import carrier as pn_carrier, geocoder
import os
from dotenv import load_dotenv

load_dotenv()

class CarrierLookupModule:
    """
    Phone lookup optimized for KSA and Global data.
    Uses NumVerify for global data and a scraper stub for KSA Numberbooks.
    """
    def __init__(self):
        self.http_client = HTTPClient()
        self.numverify_key = os.getenv("NUMVERIFY_API_KEY")

    def _ksa_phonebook_search(self, number: str) -> dict:
        """
        Public directory search for Saudi Arabia.
        """
        results = {"status": "Not Searched", "owner": "Unknown"}
        
        # In a real implementation, you would use self.http_client.post/get 
        # to query sites like 'ksanumbers.com' or other open Saudi directories.
        # Most of these use hidden APIs that require specific cookies/headers.
        
        # Example logic for a Saudi Public Phonebook API (Simulated Scraper):
        # response = self.http_client.get(f"https://open-ksa-api.com/search/{number}")
        # if response['status_code'] == 200: results['owner'] = response['data'].get('name')
        
        results["status"] = "KSA Public Directory Query Triggered"
        return results

    def scan(self, phone_number: str) -> ModuleResult:
        data = {}
        error_msg = None
        
        # Clean number for APIs
        clean_num = phone_number.replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
        full_num = "+" + clean_num if not clean_num.startswith("+") else clean_num

        # 1. Global API (NumVerify)
        if self.numverify_key:
            url = "http://apilayer.net/api/validate"
            params = {"access_key": self.numverify_key, "number": clean_num}
            response = self.http_client.get(url, params=params)
            if response["status_code"] == 200 and isinstance(response["data"], dict):
                v = response["data"]
                if v.get("valid"):
                    data["carrier"] = v.get("carrier")
                    data["location"] = f"{v.get('location')}, {v.get('country_name')}"
                    data["line_type"] = v.get("line_type")

        # 2. Regional Logic (Saudi Arabia)
        try:
            parsed = phonenumbers.parse(full_num, None)
            if parsed.country_code == 966:
                data["region"] = "Saudi Arabia"
                data["ksa_phonebook"] = self._ksa_phonebook_search(clean_num)
                # Fallback to local lib if API failed
                if "carrier" not in data:
                    data["carrier"] = pn_carrier.name_for_number(parsed, "en")
        except Exception:
            pass

        return ModuleResult(
            module_name="CarrierLookup",
            target=phone_number,
            success=len(data) > 0,
            data=data,
            confidence="HIGH" if len(data) > 2 else "LOW",
            error=error_msg
        )
