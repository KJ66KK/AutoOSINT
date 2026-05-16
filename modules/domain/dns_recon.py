from core.models import ModuleResult
from utils.http_client import HTTPClient
import dns.resolver
import shodan
import os
from dotenv import load_dotenv

load_dotenv()

class DNSReconModule:
    """
    Performs DNS reconnaissance and Shodan host analysis.
    Optimized for Shodan Student/Paid accounts.
    """
    def __init__(self):
        self.http_client = HTTPClient()
        self.shodan_api_key = os.getenv("SHODAN_API_KEY")

    def scan(self, domain: str) -> ModuleResult:
        records = {"A": [], "MX": [], "TXT": []}
        shodan_results = {}
        error_msg = None
        
        # 1. REAL DNS LOOKUP
        try:
            for rtype in ["A", "MX", "TXT"]:
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    records[rtype] = [rdata.to_text() for rdata in answers]
                except Exception:
                    pass
        except Exception as e:
            error_msg = f"DNS Error: {str(e)}"

        # 2. SHODAN ANALYSIS
        if self.shodan_api_key and records["A"]:
            try:
                api = shodan.Shodan(self.shodan_api_key)
                for ip in records["A"]:
                    # Host lookup on Shodan
                    host = api.host(ip)
                    shodan_results[ip] = {
                        "os": host.get("os", "Unknown"),
                        "ports": host.get("ports", []),
                        "services": [item.get("product", "Unknown") for item in host.get("data", [])],
                        "vulnerabilities": host.get("vulns", [])
                    }
            except Exception as e:
                # If host not found or other API error
                shodan_results[ip] = {"error": str(e)}

        success = any([records["A"], shodan_results])

        return ModuleResult(
            module_name="DNSRecon",
            target=domain,
            success=success,
            data={
                "dns_records": records,
                "shodan_intel": shodan_results
            },
            confidence="HIGH" if success else "LOW",
            error=error_msg
        )
