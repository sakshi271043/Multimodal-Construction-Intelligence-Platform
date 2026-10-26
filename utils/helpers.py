"""
Helper utilities for Multimodal Construction Intelligence Platform:
Image processing, robust JSON extraction, Indian Rupee currency formatters, and export generators.
"""

import base64
import io
import json
import re
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from PIL import Image

def image_to_base64(image_input) -> str:
    """
    Converts a PIL Image, bytes, or Streamlit UploadedFile to base64 string.
    """
    if isinstance(image_input, Image.Image):
        buffered = io.BytesIO()
        fmt = image_input.format or "JPEG"
        if fmt.upper() not in ["JPEG", "JPG", "PNG", "WEBP"]:
            fmt = "JPEG"
        image_input.convert("RGB").save(buffered, format=fmt)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    elif hasattr(image_input, "getvalue"):  # Streamlit UploadedFile
        return base64.b64encode(image_input.getvalue()).decode("utf-8")
    elif isinstance(image_input, (bytes, bytearray)):
        return base64.b64encode(image_input).decode("utf-8")
    elif isinstance(image_input, str) and image_input.startswith("data:image"):
        return image_input.split(",", 1)[-1]
    return str(image_input)

def parse_json_from_response(text: str) -> Dict[str, Any]:
    """
    Robustly extracts and parses JSON from LLM markdown code blocks or plain text.
    Handles ```json blocks, trailing commas, and nested wrappers.
    """
    if not text:
        return {}
    
    # 1. Direct parse attempt
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2. Extract inside ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        extracted = match.group(1).strip()
        try:
            return json.loads(extracted)
        except Exception:
            pass

    # 3. Outer bracket search { ... }
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except Exception:
            # Clean trailing commas
            cleaned = re.sub(r",\s*([\]}])", r"\1", candidate)
            try:
                return json.loads(cleaned)
            except Exception:
                pass

    return {"error": "Failed to parse structured JSON", "raw_output": text}

def format_inr(amount: float) -> str:
    """
    Formats currency in Indian Rupee denomination:
    - >= 1 Crore (10,000,000): '₹ XX.XX Cr'
    - >= 1 Lakh (100,000): '₹ XX.XX Lakh'
    - Else: '₹ XX,XXX'
    """
    if amount is None or amount < 0:
        return "₹ 0.00"
    
    if amount >= 10_000_000:
        cr = amount / 10_000_000.0
        return f"₹ {cr:.2f} Cr"
    elif amount >= 100_000:
        lakh = amount / 100_000.0
        return f"₹ {lakh:.2f} Lakh"
    else:
        return f"₹ {amount:,.0f}"

def format_inr_indian_commas(amount: float) -> str:
    """
    Formats a number into standard Indian comma grouping:
    e.g. 12345678 -> 1,23,45,678
    """
    s = f"{int(round(amount))}"
    if len(s) <= 3:
        return f"₹ {s}"
    last_three = s[-3:]
    remaining = s[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    parts.append(last_three)
    return "₹ " + ",".join(parts)

def get_safety_score_badge(score: int) -> Tuple[str, str, str]:
    """
    Returns (label, css_badge_class, hex_color) for safety score (0-100).
    """
    if score >= 85:
        return "Compliant (OSHA / IS 456 Approved)", "badge-emerald", "#10B981"
    elif score >= 65:
        return "Needs Attention (Minor Violations)", "badge-amber", "#F59E0B"
    else:
        return "Non-Compliant (Stop-Work Risk)", "badge-rose", "#EF4444"

def get_severity_badge_class(severity: str) -> str:
    """
    Returns CSS class for hazard severity string.
    """
    sev = (severity or "").strip().lower()
    if "crit" in sev:
        return "severity-critical"
    elif "high" in sev:
        return "severity-high"
    elif "med" in sev:
        return "severity-medium"
    else:
        return "severity-low"

def generate_audit_markdown_report(data: Dict[str, Any], project_name: str = "Active Site Inspection") -> str:
    """
    Generates a formal, printable markdown audit report.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    score = data.get("safety_score", 0)
    status = data.get("overall_status", "Needs Attention")
    workers = data.get("workers_detected", 0)
    hazards = data.get("site_hazards", [])
    ppe = data.get("ppe_detection", [])

    report = f"""# 🏗️ CONSTRUCTION SITE SAFETY & PPE COMPLIANCE AUDIT
**Project / Zone:** {project_name}  
**Timestamp:** {timestamp}  
**Auditor Engine:** Multimodal Construction Intelligence AI (OSHA 1926 & IS 456:2000 Grounded)  
**Safety Score:** {score} / 100  
**Overall Regulatory Status:** {status}  
**Active Personnel Detected:** {workers}  

---

## 🦺 PPE DETECTIONS & COMPLIANCE CHECKLIST
| Item | Status | Compliance Level | Regulatory Code | Remarks |
|---|---|---|---|---|
"""
    for item in ppe:
        report += f"| {item.get('item', 'N/A')} | {item.get('status', 'N/A')} | {item.get('compliance_rate', 'N/A')} | {item.get('code_reference', 'OSHA / IS 456')} | {item.get('notes', '')} |\n"

    report += """
---

## ⚠️ IDENTIFIED SITE HAZARDS & CORRECTIVE REMEDIES
"""
    if not hazards:
        report += "*No critical hazards identified. Site complies with core safety norms.*\n"
    else:
        for idx, h in enumerate(hazards, start=1):
            report += f"""
### Hazard #{idx}: {h.get('hazard_type', 'Unclassified')} [{h.get('severity', 'Medium').upper()}]
- **Location / Element:** {h.get('location', 'Site Perimeter')}
- **Regulatory Violation:** {h.get('regulatory_code', 'OSHA 1926 / IS 3696')}
- **Corrective Action Required:** {h.get('corrective_remedy', 'Immediate mitigation required.')}
"""

    report += f"""
---
## 📋 EXECUTIVE SUMMARY
{data.get('executive_summary', 'Routine site inspection completed. Refer to hazard remedies above.')}

---
*Report generated autonomously by Multimodal Construction Intelligence Platform — Skill Wallet Capstone Project 1.*
"""
    return report
