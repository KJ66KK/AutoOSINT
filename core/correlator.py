from typing import List, Dict, Any
from core.models import ModuleResult

class DataCorrelator:
    """
    The 'AI' component of the tool. It looks for patterns across DIFFERENT module results.
    """
    def analyze(self, results: List[ModuleResult]) -> Dict[str, Any]:
        """
        Find connections between disparate pieces of data.
        
        PRO TIP:
        Implement a 'Threat Score'. Assign points to different findings 
        (e.g., +50 for a breach, +10 for an active social account). 
        This gives investigators a quick way to prioritize targets.
        """
        insights = []
        
        # Simple correlation logic
        for result in results:
            if not result.success:
                continue
                
            if result.module_name == "DNSRecon":
                records = result.data.get("records", {})
                if not records.get("MX"):
                    insights.append("No MX records found. Domain might not receive email.")
                if len(records.get("A", [])) > 1:
                    insights.append("Multiple A records found. Potential load balancing or WAF.")
                    
            if result.module_name == "SocialScan":
                found = result.data.get("found_on", [])
                if len(found) > 2:
                    insights.append(f"Highly active username across {len(found)} platforms.")
                    
            if result.module_name == "CarrierLookup":
                if result.data.get("type") == "voip":
                    insights.append("Number is a VoIP line. Might be temporary or untraceable.")

        return {
            "insights": insights,
            "raw_results_count": len(results),
            "successful_modules": sum(1 for r in results if r.success)
        }
