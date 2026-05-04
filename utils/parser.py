"""
JSON response parser and validator for Gemini leaf-analysis output.

Handles common LLM quirks:
  - Markdown code-fence wrappers (```json ... ```)
  - Extra whitespace / trailing commas
  - Missing or mis-typed fields
"""

from __future__ import annotations

import json
import re
from typing import Any


# ---------------------------------------------------------------------------
# Expected schema
# ---------------------------------------------------------------------------
_REQUIRED_KEYS = {
    "disease_name": str,
    "confidence": str,
    "is_healthy": bool,
    "symptoms": list,
    "treatment": list,
    "prevention": list,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _strip_code_fences(text: str) -> str:
    """Remove markdown ```json ... ``` wrappers if present."""
    text = text.strip()
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return text


def _normalise_confidence(value: Any) -> str:
    """Ensure confidence is a string like '85%'."""
    if isinstance(value, (int, float)):
        return f"{int(value)}%"
    s = str(value).strip().rstrip("%")
    try:
        return f"{int(float(s))}%"
    except (ValueError, TypeError):
        return "N/A"


def _confidence_to_int(confidence_str: str) -> int:
    """Convert a confidence string like '85%' to an integer 0-100."""
    try:
        return max(0, min(100, int(confidence_str.rstrip("%"))))
    except (ValueError, TypeError):
        return 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def parse_response(raw_text: str) -> dict | None:
    """Parse and validate the Gemini JSON response.

    Parameters
    ----------
    raw_text : str
        Raw text from the Gemini API.

    Returns
    -------
    dict | None
        Validated result dict with keys:
          disease_name, confidence, confidence_pct, is_healthy,
          symptoms, treatment, prevention.
        Returns ``None`` if parsing fails entirely.
    """
    cleaned = _strip_code_fences(raw_text)

    try:
        data: dict = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    # Validate required keys – fill missing ones with defaults
    result: dict[str, Any] = {}
    for key, expected_type in _REQUIRED_KEYS.items():
        value = data.get(key)
        if value is None or not isinstance(value, expected_type):
            if expected_type is str:
                value = "Unknown"
            elif expected_type is bool:
                value = False
            elif expected_type is list:
                value = []
        result[key] = value

    # Normalise confidence
    result["confidence"] = _normalise_confidence(result["confidence"])
    result["confidence_pct"] = _confidence_to_int(result["confidence"])

    return result
