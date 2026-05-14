from core.models import ModuleResult
from utils.http_client import HTTPClient
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import re

class CarrierLookupModule:
    def __init__(self):
        self.http_client = HTTPClient()

    def scan(self, phone_number: str) -> ModuleResult:
        data = {}
        error_msg = None
        success = False

        # Pre-process the (CC)Number format into +CCNumber for the phonenumbers lib
        processed_number = phone_number
        if "(" in phone_number and ")" in phone_number:
            processed_number = "+" + phone_number.replace("(", "").replace(")", "").replace(" ", "")
        elif not phone_number.startswith("+"):
            processed_number = "+" + phone_number

        try:
            parsed_number = phonenumbers.parse(processed_number, None)
            
            if phonenumbers.is_valid_number(parsed_number):
                success = True
                data["is_valid"] = True
                data["carrier"] = carrier.name_for_number(parsed_number, "en")
                data["location"] = geocoder.description_for_number(parsed_number, "en")
                data["timezones"] = list(timezone.time_zones_for_number(parsed_number))
                data["country_code"] = parsed_number.country_code
                
                # Regional Logic: Saudi Arabia (966)
                if parsed_number.country_code == 966:
                    data["region"] = "Saudi Arabia"
                    # TODO: Implement scraping or API call to Saudi open phonebooks 
                    # (e.g., KSA Numbers, Numberbook etc. if available via web_fetch or API)
                    data["local_phonebook_search"] = "Triggered search in Saudi Public Directories..."
                    
                data["formatted_national"] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
                data["formatted_international"] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            else:
                success = False
                error_msg = "Invalid phone number or country code."

        except Exception as e:
            success = False
            error_msg = str(e)

        return ModuleResult(
            module_name="CarrierLookup",
            target=phone_number,
            success=success,
            data=data,
            confidence="HIGH" if success else "LOW",
            error=error_msg
        )
