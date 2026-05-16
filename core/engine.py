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

    def run_all(self, target: str, target_type: str, recursive: bool = False, visited: set = None) -> List[ModuleResult]:
        """
        Runs all modules and optionally follows 'pivots' to scan linked data.
        """
        if visited is None:
            visited = set()
        
        # Prevent infinite loops
        state_key = f"{target_type}:{target}"
        if state_key in visited:
            return []
        visited.add(state_key)

        results = []
        applicable_modules = self.modules.get(target_type, [])

        for module in applicable_modules:
            try:
                result = module.scan(target)
                results.append(result)
                
                # RECURSIVE PIVOT LOGIC
                if recursive and result.pivots:
                    for pivot in result.pivots:
                        pivot_results = self.run_all(
                            pivot["value"], 
                            pivot["type"], 
                            recursive=True, 
                            visited=visited
                        )
                        results.extend(pivot_results)
                        
            except Exception as e:
                results.append(ModuleResult(
                    module_name=module.__class__.__name__,
                    target=target,
                    success=False,
                    data={},
                    error=f"Module crashed: {str(e)}"
                ))

        return results
