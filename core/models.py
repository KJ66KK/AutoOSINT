from pydantic import BaseModel
from typing import Optional, Any, Dict

class ModuleResult(BaseModel):
    """
    Standardized result model for all AutoOSINT modules.
    
    EXPANSION POINT:
    If you want to add new global fields (like 'execution_time' or 'api_quota_remaining'), 
    add them here as Optional fields.
    """
    module_name: str
    target: str
    success: bool
    data: Dict[str, Any]  # Key findings go here (e.g., {'ip': '1.2.3.4'})
    confidence: str = "LOW"  # LOW, MEDIUM, HIGH
    error: Optional[str] = None
