import json
import csv
import os
from typing import List
from core.models import ModuleResult

# Ensure output directories exist
os.makedirs("output/results", exist_ok=True)
os.makedirs("output/logs", exist_ok=True)

# EXPANSION POINT:
# To add a NEW export format (e.g., HTML or PDF):
# 1. Create a function 'export_to_html(results, filename)'.
# 2. Use a library like 'jinja2' for HTML or 'reportlab' for PDF.
# 3. Add the flag to 'cli.py' to trigger it.

def export_to_json(results: List[ModuleResult], filename: str = "output/results/scan_result.json"):
    data = [result.model_dump() for result in results]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return filename

def export_to_csv(results: List[ModuleResult], filename: str = "output/results/scan_result.csv"):
    if not results:
        return filename

    # Basic flattening for CSV
    headers = ["module_name", "target", "success", "confidence", "error", "data_summary"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in results:
            row = {
                "module_name": r.module_name,
                "target": r.target,
                "success": r.success,
                "confidence": r.confidence,
                "error": r.error,
                "data_summary": json.dumps(r.data) # Storing dict as JSON string in CSV cell
            }
            writer.writerow(row)
    return filename
