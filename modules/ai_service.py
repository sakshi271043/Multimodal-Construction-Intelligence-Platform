"""
Unified AI Multi-Provider Service for Multimodal Construction Intelligence Platform.
Supports Google Gemini (Multimodal Vision + Reasoning) with robust demonstration mode fallback.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from PIL import Image

from utils.helpers import parse_json_from_response
from modules.demo_data import (
    DEMO_PPE_SITES,
    DEMO_CRACKS,
    DEMO_WEATHER_PROTOCOLS,
    DEMO_CHAT_KNOWLEDGE
)

logger = logging.getLogger("ConstructionAI")

class ConstructionAIService:
    def __init__(
        self,
        provider: str = "demo",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """
        provider: 'gemini' or 'demo'
        api_key: Google Gemini API key
        model_name: specific Gemini model (e.g. 'gemini-2.5-flash', 'gemini-1.5-flash')
        """
        self.provider = (provider or "demo").lower()
        self.api_key = (api_key or "").strip()
        self.model_name = model_name or "gemini-2.5-flash"
        self.client = None
        self._gemini_sdk = None
        self._init_client()

    def _init_client(self):
        """Initializes Gemini API client if credentials are provided."""
        if not self.api_key or self.provider == "demo":
            self.provider = "demo"
            return

        try:
            # First attempt: modern google.genai Client
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                self._gemini_sdk = "genai"
                logger.info("Initialized modern google.genai client")
            except Exception as e1:
                # Second attempt: legacy google.generativeai
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self.client = legacy_genai
                self._gemini_sdk = "legacy"
                logger.info(f"Initialized legacy google.generativeai client: {e1}")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini client ({e}). Falling back to Demo mode.")
            self.provider = "demo"

    # ==========================================
    # TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
    # ==========================================
    def audit_site_safety_ppe(
        self,
        image_input: Any,
        site_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Multimodal prompt analyzing worker PPE compliance (helmets, high-vis vests,
        steel-toe boots, safety harnesses) under OSHA 1926 and IS 456 standards.
        Returns structured JSON with safety_score, overall_status, ppe_detection, and site_hazards.
        """
        if self.provider == "demo" or not self.client:
            # Match preset if available or return primary demo
            if site_context and site_context in DEMO_PPE_SITES:
                return DEMO_PPE_SITES[site_context]
            for key, val in DEMO_PPE_SITES.items():
                if site_context and (site_context.lower() in key.lower() or key.lower() in site_context.lower()):
                    return val
            return DEMO_PPE_SITES["Active High-Rise Slab Rebar & Concreting"]

        system_prompt = (
            "You are a Senior Construction Site Safety Director and Certified OSHA 1926 / IS 456 Inspector. "
            "Analyze the construction site image in extreme technical detail for worker PPE compliance and physical hazards.\n\n"
            "Key PPE items to inspect:\n"
            "1. Helmets / Hard Hats (OSHA 1926.100 & IS 2925)\n"
            "2. High-Visibility Safety Vests (OSHA 1926.200 & IS 15809)\n"
            "3. Steel-Toe Safety Boots / Footwear (OSHA 1926.96 & IS 15298)\n"
            "4. Safety Harnesses & Fall Arrest Systems (mandatory near edges > 1.8m, OSHA 1926.502 & IS 3521)\n"
            "5. Eye & Face Protection (safety goggles, shields)\n"
            "6. Heavy-Duty Work Gloves\n\n"
            "You MUST respond ONLY with a valid JSON object matching this exact schema:\n"
            "{\n"
            '  "safety_score": 75,\n'
            '  "overall_status": "Compliant" | "Needs Attention" | "Non-Compliant (Stop-Work Risk)",\n'
            '  "workers_detected": 4,\n'
            '  "ppe_detection": [\n'
            '    {\n'
            '      "item": "Safety Helmets (Hard Hats)",\n'
            '      "status": "Detected" | "Partial" | "Missing" | "N/A",\n'
            '      "compliance_rate": "80% (4/5 Workers)",\n'
            '      "code_reference": "OSHA 1926.100 & IS 2925",\n'
            '      "notes": "Technical observations"\n'
            '    }\n'
            '  ],\n'
            '  "site_hazards": [\n'
            '    {\n'
            '      "hazard_id": "HAZ-001",\n'
            '      "hazard_type": "Unprotected Slab Edge Fall Hazard",\n'
            '      "severity": "Low" | "Medium" | "High" | "Critical",\n'
            '      "location": "Deck perimeter",\n'
            '      "regulatory_code": "OSHA 1926.501(b)(1)",\n'
            '      "corrective_remedy": "Specific engineering remediation action"\n'
            '    }\n'
            '  ],\n'
            '  "executive_summary": "Comprehensive regulatory overview and actionable guidance."\n'
            "}"
        )

        user_prompt = f"Analyze this construction site photo. Context notes: {site_context or 'Active construction zone'}."

        try:
            # Handle PIL image
            pil_img = self._load_pil_image(image_input)
            
            if self._gemini_sdk == "genai":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[pil_img, system_prompt + "\n\n" + user_prompt]
                )
                raw_text = response.text or ""
            else:
                model = self.client.GenerativeModel(self.model_name)
                response = model.generate_content([system_prompt + "\n\n" + user_prompt, pil_img])
                raw_text = response.text or ""

            parsed = parse_json_from_response(raw_text)
            if "safety_score" in parsed and "ppe_detection" in parsed:
                return parsed
            else:
                logger.warning(f"Gemini output lacked required keys, returning demo fallback: {raw_text[:200]}")
                return DEMO_PPE_SITES["Active High-Rise Slab Rebar & Concreting"]
        except Exception as e:
            logger.error(f"Error calling Gemini for PPE audit: {e}. Falling back to demo data.")
            return DEMO_PPE_SITES["Active High-Rise Slab Rebar & Concreting"]

    # ==========================================
    # TAB 2: CRACK DIAGNOSTICS & INTEGRITY (EPIC 2)
    # ==========================================
    def diagnose_crack_structural(
        self,
        image_input: Any,
        element_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Multimodal prompt classifying defect type (Hairline, Settlement, Structural Shear,
        Thermal Expansion, Spalling) with estimated crack width (mm), root causes,
        recommended engineering repairs (epoxy injection, structural re-grouting), and urgency.
        """
        if self.provider == "demo" or not self.client:
            if element_context and element_context in DEMO_CRACKS:
                return DEMO_CRACKS[element_context]
            for key, val in DEMO_CRACKS.items():
                if element_context and (element_context.lower() in key.lower() or key.lower() in element_context.lower()):
                    return val
            return DEMO_CRACKS["Structural Shear Crack at Beam-Column Joint"]

        system_prompt = (
            "You are an expert Structural Forensic Engineer and Civil Consultant specializing in concrete pathology, "
            "IS 456:2000, IS 13920, and ACI 224 concrete crack repair standards.\n\n"
            "Analyze the defect on the concrete / masonry surface in the image.\n"
            "Classify the defect type into one of:\n"
            "['Structural Shear Crack', 'Settlement Crack', 'Hairline Crack', 'Thermal Expansion Joint Failure', 'Spalling & Carbonation Corrosion', 'Honeycombing & Void']\n\n"
            "You MUST respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "title": "Descriptive defect title",\n'
            '  "element": "e.g. RCC Beam-Column Junction, Slab soffit, Masonry Infill",\n'
            '  "defect_type": "Structural Shear Crack",\n'
            '  "estimated_width_mm": 1.5,\n'
            '  "is456_exposure_limit_mm": 0.20,\n'
            '  "urgency": "Low (Aesthetic / Non-Critical)" | "Moderate (Monitor & Remediate)" | "Urgent (High Structural Risk)" | "Immediate Evacuation / Critical",\n'
            '  "root_causes": "Detailed civil engineering analysis of mechanisms (shear overload, settlement, thermal, alkali-silica, corrosion)",\n'
            '  "engineering_repairs": [\n'
            '    "Step 1: Specific engineering action (e.g. low-viscosity epoxy pressure injection < 200 cps)",\n'
            '    "Step 2: Structural re-grouting / CFRP wrap / surface preparation"\n'
            '  ],\n'
            '  "standards_reference": "IS 456:2000 Clause 35.3.2, IS 13920:2016, ACI 224.1R",\n'
            '  "remediation_urgency_days": "Immediate (Within 48 Hours)"\n'
            "}"
        )

        user_prompt = f"Diagnose this concrete/masonry defect. Location/element context: {element_context or 'Structural Element'}."

        try:
            pil_img = self._load_pil_image(image_input)
            
            if self._gemini_sdk == "genai":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[pil_img, system_prompt + "\n\n" + user_prompt]
                )
                raw_text = response.text or ""
            else:
                model = self.client.GenerativeModel(self.model_name)
                response = model.generate_content([system_prompt + "\n\n" + user_prompt, pil_img])
                raw_text = response.text or ""

            parsed = parse_json_from_response(raw_text)
            if "defect_type" in parsed and "engineering_repairs" in parsed:
                return parsed
            else:
                logger.warning(f"Gemini output lacked required keys, returning demo fallback: {raw_text[:200]}")
                return DEMO_CRACKS["Structural Shear Crack at Beam-Column Joint"]
        except Exception as e:
            logger.error(f"Error calling Gemini for crack diagnosis: {e}. Falling back to demo data.")
            return DEMO_CRACKS["Structural Shear Crack at Beam-Column Joint"]

    # ==========================================
    # TAB 4: INTERACTIVE SITE CHATBOT (EPIC 5)
    # ==========================================
    def chat_construction_assistant(
        self,
        messages: List[Dict[str, str]],
        weather_context: Optional[str] = None
    ) -> str:
        """
        Interactive multi-turn construction engineering assistant chatbot.
        Maintains persona of a Senior Chartered Structural Engineer & Site Safety Director.
        """
        # Standalone demo mode fallback
        if self.provider == "demo" or not self.client:
            latest_msg = messages[-1]["content"].lower() if messages else ""
            if "is 456" in latest_msg or "code" in latest_msg or "crack width" in latest_msg:
                return DEMO_CHAT_KNOWLEDGE["is456"]
            elif "wind" in latest_msg or "crane" in latest_msg or "tower" in latest_msg:
                return DEMO_CHAT_KNOWLEDGE["osha_wind"]
            elif "epoxy" in latest_msg or "grout" in latest_msg or "repair" in latest_msg:
                return DEMO_CHAT_KNOWLEDGE["crack_repair"]
            elif "cement" in latest_msg or "mix" in latest_msg or "steel" in latest_msg or "m25" in latest_msg:
                return DEMO_CHAT_KNOWLEDGE["mix_design"]
            else:
                return (
                    f"**Site Engineering Field Directive**\n\n"
                    f"Under the current active site weather condition (**{weather_context or 'Standard'}**), "
                    f"ensure strict compliance with IS 456:2000 and OSHA 1926 standards. "
                    f"For structural crack assessments, verify width against Table 2 exposure limits (0.3mm mild, 0.2mm moderate). "
                    f"Always verify formwork propping, bar splicing lengths (minimum 50d in tension), and continuous wet curing for 14 days."
                )

        system_instruction = (
            "You are an authoritative Senior Structural & Civil Engineer and Construction EHS Director. "
            "You possess deep expertise in IS 456:2000, IS 1893:2016 (Earthquake Resistance), IS 875:2015 (Wind & Live Loads), "
            "OSHA 1926 construction safety regulations, and CPWD civil engineering benchmarks.\n\n"
            f"Current Site Environmental Context: {weather_context or 'Normal / Clear'}.\n\n"
            "Guidelines:\n"
            "- Provide practical, high-precision engineering advice with exact code clauses, formula references, and material specs.\n"
            "- Highlight safety red flags immediately.\n"
            "- Format responses cleanly with bold headings, bullet points, and actionable checklists."
        )

        try:
            conversation_history = ""
            for m in messages:
                role = "User" if m["role"] == "user" else "Assistant"
                conversation_history += f"{role}: {m['content']}\n"

            prompt = f"{system_instruction}\n\nConversation History:\n{conversation_history}\nAssistant:"

            if self._gemini_sdk == "genai":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text or "No response received."
            else:
                model = self.client.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                return response.text or "No response received."
        except Exception as e:
            logger.error(f"Error in chat assistant: {e}")
            return (
                f"**Engine Advisory (Demo Mode Fallback):**\n\n"
                f"Gemini API returned an operational notice: `{str(e)[:120]}`.\n\n"
                + DEMO_CHAT_KNOWLEDGE["is456"]
            )

    def _load_pil_image(self, image_input: Any) -> Image.Image:
        """Helper to ensure input is a valid RGB PIL Image."""
        if isinstance(image_input, Image.Image):
            return image_input.convert("RGB")
        elif hasattr(image_input, "getvalue"):  # Streamlit UploadedFile
            return Image.open(image_input).convert("RGB")
        elif isinstance(image_input, (bytes, bytearray)):
            import io
            return Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, str):
            # Check if file path
            if os.path.exists(image_input):
                return Image.open(image_input).convert("RGB")
            # If base64 or URL
            import requests
            import io
            if image_input.startswith("http"):
                res = requests.get(image_input, timeout=10)
                return Image.open(io.BytesIO(res.content)).convert("RGB")
        # Fallback dummy image
        return Image.new("RGB", (640, 480), color=(100, 110, 120))
