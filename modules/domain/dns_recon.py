from core.models import ModuleResult
import dns.resolver

class DNSReconModule:
    """
    Performs DNS reconnaissance using the 'dnspython' library.
    """
    def scan(self, domain: str) -> ModuleResult:
        # PRO TIP:
        # To find 'hidden' subdomains (e.g., dev.site.com), create a list of common 
        # prefixes (admin, mail, vpn, api) and loop through them, trying to resolve 
        # each one. This is called 'Subdomain Brute-forcing'.
        
        # EXPANSION POINT:
        # To add NEW records (e.g., CNAME, SOA, NS):
        # 1. Add the record type to the 'records' dictionary below.
        # 2. Add a new try/except block to perform the lookup.
        records = {"A": [], "MX": [], "TXT": []}
        error_msg = None
        success = False

        try:
            # A Records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                records["A"] = [rdata.to_text() for rdata in answers]
            except Exception:
                pass

            # MX Records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                records["MX"] = [rdata.to_text() for rdata in answers]
            except Exception:
                pass

            # TXT Records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                records["TXT"] = [rdata.to_text() for rdata in answers]
            except Exception:
                pass

            success = any(len(v) > 0 for v in records.values())
        except Exception as e:
            error_msg = str(e)
            success = False

        return ModuleResult(
            module_name="DNSRecon",
            target=domain,
            success=success,
            data={
                "records": records
            },
            confidence="HIGH" if success else "LOW",
            error=error_msg
        )
