"""
Helper utilities for Food Verse AI:
Image conversion, robust JSON parsing, data sanitation, and report generators.
"""

import base64
import io
import json
import re
from typing import Any, Dict, Optional
from PIL import Image

def image_to_base64(image_input) -> str:
    """
    Converts a PIL Image, bytes, or UploadedFile to base64 string.
    """
    if isinstance(image_input, Image.Image):
        buffered = io.BytesIO()
        # Save as PNG or JPEG
        fmt = image_input.format or "PNG"
        image_input.save(buffered, format=fmt)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    elif hasattr(image_input, "getvalue"):  # Streamlit UploadedFile
        return base64.b64encode(image_input.getvalue()).decode("utf-8")
    elif isinstance(image_input, (bytes, bytearray)):
        return base64.b64encode(image_input).decode("utf-8")
    elif isinstance(image_input, str) and image_input.startswith("data:image"):
        # Strip header if present
        return image_input.split(",", 1)[-1]
    return str(image_input)

def parse_json_from_response(text: str) -> Dict[str, Any]:
    """
    Robustly extracts and parses JSON from LLM markdown code blocks or text.
    Handles ```json blocks, trailing commas, and partial wrappers.
    """
    if not text:
        return {}
    
    # Try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting inside ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        extracted = match.group(1).strip()
        try:
            return json.loads(extracted)
        except Exception:
            pass

    # Try finding outer { ... }
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except Exception:
            # Clean common trailing commas before closing braces
            cleaned = re.sub(r",\s*([\]}])", r"\1", candidate)
            try:
                return json.loads(cleaned)
            except Exception:
                pass

    return {"error": "Failed to parse structured JSON", "raw_output": text}

def get_health_score_badge(score: int) -> tuple[str, str, str]:
    """
    Returns (label, color_class, hex_color) for a health score (1-100).
    """
    if score >= 85:
        return "Optimal Superfood", "badge-emerald", "#10B981"
    elif score >= 70:
        return "Nutrient Dense", "badge-cyan", "#06B6D4"
    elif score >= 50:
        return "Moderate Balance", "badge-amber", "#F59E0B"
    else:
        return "Indulgent / High Limit", "badge-rose", "#EF4444"

def get_freshness_badge(stage: str) -> tuple[str, str, str]:
    """
    Returns (label, css_class, hex_color) for freshness stage.
    """
    stage_lower = (stage or "").lower()
    if "fresh" in stage_lower and "moderately" not in stage_lower:
        return "Fresh (Safe to Eat)", "badge-emerald", "#10B981"
    elif "moderately" in stage_lower or "moderate" in stage_lower:
        return "Moderately Fresh (Consume Promptly)", "badge-amber", "#F59E0B"
    else:
        return "Spoiled (Hazard - Discard)", "badge-rose", "#EF4444"

def get_hygiene_score_badge(score: int) -> tuple[str, str, str]:
    """
    Returns (rating_grade, css_class, hex_color) for Kitchen Hygiene compliance score.
    """
    if score >= 90:
        return "Grade A+ (Exemplary Compliance)", "badge-emerald", "#10B981"
    elif score >= 80:
        return "Grade A (Meets HACCP Standard)", "badge-cyan", "#06B6D4"
    elif score >= 70:
        return "Grade B (Minor Corrections Required)", "badge-amber", "#F59E0B"
    else:
        return "Grade C / Fail (Critical Violation)", "badge-rose", "#EF4444"
