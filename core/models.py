from pydantic import BaseModel
from typing import Optional, Any, Dict, List

class ModuleResult(BaseModel):
    """
    Standardized result model for all AutoOSINT modules.
    """
    module_name: str
    target: str
    success: bool
    data: Dict[str, Any]
    pivots: List[Dict[str, str]] = []  # List of linked targets found: [{"type": "email", "value": "test@site.com"}]
    confidence: str = "LOW"
    error: Optional[str] = None
