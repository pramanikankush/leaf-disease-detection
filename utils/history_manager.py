import json
import os
from datetime import datetime
from typing import List, Dict, Any

HISTORY_FILE = os.path.join("data", "history.json")

def _ensure_data_dir():
    os.makedirs("data", exist_ok=True)

def save_record(parsed_result: Dict[str, Any], severity_score: int = 50):
    """Save a new diagnosis record to history.
    
    Parameters
    ----------
    parsed_result : Dict[str, Any]
        The parsed diagnosis result from Gemini
    severity_score : int
        Severity score 0-100 (0=healthy, 100=critical)
    """
    if not parsed_result:
        return
        
    _ensure_data_dir()
    
    records = get_history()
    
    # Create a new record with a timestamp
    record = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "disease_name": parsed_result.get("disease_name", "Unknown"),
        "confidence": parsed_result.get("confidence", "N/A"),
        "is_healthy": parsed_result.get("is_healthy", False),
        "symptoms": parsed_result.get("symptoms", []),
        "treatment": parsed_result.get("treatment", []),
        "prevention": parsed_result.get("prevention", []),
        "severity_score": severity_score
    }
    
    records.insert(0, record) # Insert at beginning
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def get_history() -> List[Dict[str, Any]]:
    """Retrieve all history records."""
    if not os.path.exists(HISTORY_FILE):
        return []
        
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def clear_history():
    """Clear all history records."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
