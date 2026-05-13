import json
from typing import List
from core.models import ModuleResult

def export_to_json(results: List[ModuleResult], filename: str):
    # TODO: Convert the list of ModuleResult objects (Pydantic models) into a JSON string
    # and write it to the output/results/ directory.
    # Hint: Pydantic has a built-in .model_dump() method.
    pass

def export_to_csv(results: List[ModuleResult], filename: str):
    # TODO: Implement CSV exporting. You might need to flatten the 'data' dictionary
    # so it fits nicely into columns.
    pass
