from pydantic import BaseModel
from typing import Optional, Any, Dict

class ModuleResult(BaseModel):
    module_name: str
    target: str
    success: bool
    data: Dict[str, Any]
    confidence: str = "LOW"  # LOW, MEDIUM, HIGH
    error: Optional[str] = None
