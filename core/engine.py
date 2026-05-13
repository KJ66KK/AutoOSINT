from typing import List
from core.models import ModuleResult

class ScannerEngine:
    def __init__(self):
        # TODO: Initialize your modules here, or implement a dynamic loader
        # that scans the 'modules/' directory and loads classes automatically.
        self.active_modules = []

    def run_all(self, target: str, target_type: str) -> List[ModuleResult]:
        """
        Run all applicable modules for a given target type.
        """
        results = []
        # TODO: 
        # 1. Filter self.active_modules based on target_type.
        # 2. Loop through the applicable modules and call their .scan(target) method.
        # 3. Append the ModuleResult to the results list.
        # 4. Handle exceptions so if one module crashes, the engine keeps running.
        return results
