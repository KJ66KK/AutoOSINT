from typing import List
from core.models import ModuleResult

# Import modules
from modules.email.breach_check import EmailBreachModule
from modules.domain.dns_recon import DNSReconModule
from modules.phone.carrier_lookup import CarrierLookupModule
from modules.username.social_scan import SocialScanModule

class ScannerEngine:
    """
    The central orchestration engine. It decides which modules run for which target.
    """
    def __init__(self):
        # EXPANSION POINT:
        # To add a NEW module:
        # 1. Import your module class at the top of this file.
        # 2. Add it to the list in self.modules[target_type].
        self.modules = {
            "email": [EmailBreachModule()],
            "domain": [DNSReconModule()],
            "phone": [CarrierLookupModule()],
            "username": [SocialScanModule()]
        }

    def run_all(self, target: str, target_type: str) -> List[ModuleResult]:
        """
        Runs all modules registered for a specific target_type.
        
        PRO TIP: 
        To make this 10x faster, use 'concurrent.futures.ThreadPoolExecutor' 
        to run 'module.scan' in parallel threads. OSINT is mostly network-bound!
        """
        results = []
        applicable_modules = self.modules.get(target_type, [])
        
        # If it's a username, maybe we also want to run it against some email parts? 
        # Keeping it simple for now based on target_type.

        for module in applicable_modules:
            try:
                result = module.scan(target)
                results.append(result)
            except Exception as e:
                # Catch-all to prevent one module crashing the whole scan
                results.append(ModuleResult(
                    module_name=module.__class__.__name__,
                    target=target,
                    success=False,
                    data={},
                    error=f"Module crashed: {str(e)}"
                ))

        return results
