"""
Unified AI Multi-Provider Service for Food Verse AI.
Supports Google Gemini (Multimodal Vision + Reasoning), Groq, and Standalone Showcase / Demo fallback.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from PIL import Image

from utils.helpers import image_to_base64, parse_json_from_response
from modules.demo_data import (
    DEMO_NUTRITION_ITEMS,
    DEMO_FRESHNESS_ITEMS,
    DEMO_HYGIENE_INSPECTIONS,
    DEMO_RECIPES
)

logger = logging.getLogger("FoodVerseAI")

class FoodVerseAIService:
    def __init__(
        self,
        provider: str = "demo",
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """
        provider: 'gemini', 'groq', or 'demo'
        api_key: API key string if using real LLM
        model_name: Optional specific model name
        """
        self.provider = provider.lower() if provider else "demo"
        self.api_key = (api_key or "").strip()
        self.model_name = model_name
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initializes the active provider client if credentials exist."""
        if not self.api_key or self.provider == "demo":
            self.provider = "demo"
            return

        try:
            if self.provider == "gemini":
                # Check for google-genai or google-generativeai
                try:
                    from google import genai
                    self.client = genai.Client(api_key=self.api_key)
                    self._gemini_sdk = "genai"
                except Exception:
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=self.api_key)
                    self.client = legacy_genai
                    self._gemini_sdk = "legacy"
            elif self.provider == "groq":
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
        except Exception as e:
            logger.warning(f"Failed to initialize {self.provider} client: {e}. Falling back to Demo mode.")
            self.provider = "demo"

    # ==========================================
    # TAB 1: FOOD RECOGNITION & NUTRITION AUDIT
    # ==========================================
    def analyze_nutrition(
        self,
        image_input: Any,
        dish_name_hint: Optional[str] = None,
        portion_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Multimodal food recognition, nutritional breakdown, macro calculation,
        and composite Health Score (1-100).
        """
        if self.provider == "demo" or not self.client:
            # Match closest demo item or return default
            if dish_name_hint and dish_name_hint in DEMO_NUTRITION_ITEMS:
                return DEMO_NUTRITION_ITEMS[dish_name_hint]
            for key, val in DEMO_NUTRITION_ITEMS.items():
                if dish_name_hint and (dish_name_hint.lower() in key.lower() or key.lower() in dish_name_hint.lower()):
                    return val
            # Default to Mediterranean bowl
            return DEMO_NUTRITION_ITEMS["Mediterranean Salmon & Quinoa Bowl"]

        system_prompt = (
            "You are Food Verse AI, an elite Food Scientist and Registered Dietitian. "
            "Analyze the meal or dish in the image and provide a rigorous nutritional audit. "
            "Respond ONLY with a valid JSON object matching this exact schema:\n"
            "{\n"
            '  "dish_name": "Accurate culinary name of dish",\n'
            '  "cuisine": "Culinary tradition or origin",\n'
            '  "portion_size": "Estimated portion weight in grams and household measure",\n'
            '  "calories_kcal": 550,\n'
            '  "protein_g": 35.0,\n'
            '  "carbohydrates_g": 45.0,\n'
            '  "fats_g": 20.0,\n'
            '  "fiber_g": 8.5,\n'
            '  "sugar_g": 4.0,\n'
            '  "sodium_mg": 520,\n'
            '  "health_score": 92,\n'
            '  "dietary_flags": ["High Protein", "Gluten-Free Friendly"],\n'
            '  "allergen_alerts": ["Dairy", "Nuts"],\n'
            '  "ingredients": [\n'
            '     {"name": "Ingredient Name", "weight_g": 150, "calories": 220}\n'
            '  ],\n'
            '  "dietitian_review": "Comprehensive scientific assessment of macronutrient balance and micronutrient bio-availability.",\n'
            '  "optimization_tip": "Specific actionable suggestion to enhance nutrition density."\n'
            "}\n"
            "Health score must be an integer between 1 and 100 based on whole food composition, fiber, protein vs ultra-processed saturated fats and added sugars."
        )

        user_content = f"Analyze this meal. Optional dish context: {dish_name_hint or 'None'}. Portion hint: {portion_hint or 'Standard single serving'}."

        try:
            return self._call_multimodal_vision(image_input, system_prompt, user_content)
        except Exception as e:
            logger.error(f"Error calling AI vision for nutrition: {e}")
            fallback = DEMO_NUTRITION_ITEMS.get(dish_name_hint, DEMO_NUTRITION_ITEMS["Mediterranean Salmon & Quinoa Bowl"]).copy()
            fallback["dietitian_review"] += f" (Note: Simulated audit triggered due to API error: {str(e)[:70]}...)"
            return fallback

    # ==========================================
    # TAB 2: FOOD FRESHNESS & SPOILAGE DIAGNOSTIC
    # ==========================================
    def analyze_freshness(
        self,
        image_input: Any,
        item_name_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Multimodal spoilage diagnostic evaluating surface texture, discoloration,
        wrinkling, and mold. Classifies freshness: [Fresh | Moderately Fresh | Spoiled].
        """
        if self.provider == "demo" or not self.client:
            if item_name_hint and item_name_hint in DEMO_FRESHNESS_ITEMS:
                return DEMO_FRESHNESS_ITEMS[item_name_hint]
            for key, val in DEMO_FRESHNESS_ITEMS.items():
                if item_name_hint and (item_name_hint.lower() in key.lower() or key.lower() in item_name_hint.lower()):
                    return val
            return DEMO_FRESHNESS_ITEMS["Fresh Hass Avocado"]

        system_prompt = (
            "You are Food Verse AI, an expert post-harvest food scientist and microbiologist. "
            "Inspect the perishable food item in the image for spoilage, cellular breakdown, and pathogens. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "item_name": "Scientific/Common name of the food item",\n'
            '  "category": "Produce / Meat / Dairy / Bakery / Poultry",\n'
            '  "freshness_stage": "Fresh" OR "Moderately Fresh" OR "Spoiled",\n'
            '  "freshness_index": 85,\n'
            '  "surface_evaluation": {\n'
            '     "texture": "Evaluation of firmness, turgor pressure, softening, or slime",\n'
            '     "discoloration": "Evaluation of browning, oxidation, or pigment loss",\n'
            '     "wrinkling": "Evaluation of epidermal moisture loss and shrinkage",\n'
            '     "mold_status": "Evaluation of fungal mycelium, sporulation, or bacterial colonies"\n'
            '  },\n'
            '  "food_safety_advice": "Explicit safety status: Safe to consume | Consume within 24 hours | Discard immediately",\n'
            '  "shelf_life_remaining": "Estimated remaining consumable shelf life",\n'
            '  "storage_tips": ["Preservation storage tip 1", "Preservation storage tip 2"],\n'
            '  "salvage_tips": "Zero-waste culinary salvage tips if moderately fresh, or disposal advice if spoiled"\n'
            "}\n"
            "Freshness index is 0 (heavily spoiled) to 100 (freshly harvested/butchered)."
        )

        user_content = f"Evaluate this perishable food item. User item hint: {item_name_hint or 'Raw perishable item'}."

        try:
            return self._call_multimodal_vision(image_input, system_prompt, user_content)
        except Exception as e:
            logger.error(f"Error calling AI vision for freshness: {e}")
            fallback = DEMO_FRESHNESS_ITEMS.get(item_name_hint, DEMO_FRESHNESS_ITEMS["Fresh Hass Avocado"]).copy()
            fallback["food_safety_advice"] += f" (Simulated fallback due to API status: {str(e)[:60]})"
            return fallback

    # ==========================================
    # TAB 3: KITCHEN HYGIENE & FOOD SAFETY AUDIT
    # ==========================================
    def audit_kitchen_hygiene(
        self,
        image_input: Any,
        facility_type: Optional[str] = "Commercial Kitchen"
    ) -> Dict[str, Any]:
        """
        Visual inspection for commercial/domestic kitchens:
        Hairnet compliance, glove usage, sanitization state, cross-contamination,
        and compliance score (%) with itemized violation logs.
        """
        if self.provider == "demo" or not self.client:
            if "Critical" in (facility_type or "") or "Violation" in (facility_type or ""):
                return DEMO_HYGIENE_INSPECTIONS["Commercial Prep Kitchen - Critical Violation"]
            return DEMO_HYGIENE_INSPECTIONS["Commercial Prep Kitchen - Critical Violation"]

        system_prompt = (
            "You are Food Verse AI, an accredited Public Health Food Safety Auditor and HACCP Inspector. "
            "Audit the commercial kitchen or food prep environment shown in the image. "
            "Inspect for: 1) Chef hats/hairnets and beard restraints, 2) Glove usage and hand hygiene PPE, "
            "3) Surface cleanliness and sanitization, 4) Cross-contamination hazards (e.g. raw poultry/meat touching produce). "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "scene_name": "Description of inspected kitchen station",\n'
            '  "facility_type": "Commercial Kitchen / Cloud Kitchen / Food Truck",\n'
            '  "compliance_score": 82,\n'
            '  "compliance_grade": "Grade A" OR "Grade B" OR "Grade C / Fail",\n'
            '  "detected_indicators": {\n'
            '     "hair_restraint_compliance": "Compliant / Violation details",\n'
            '     "glove_ppe_compliance": "Compliant / Violation details",\n'
            '     "surface_sanitization": "Clean / Debris / Stained details",\n'
            '     "cross_contamination_hazard": "Identification of any cross-contact risk"\n'
            '  },\n'
            '  "violations": [\n'
            '     {\n'
            '       "severity": "Critical" OR "Major" OR "Minor",\n'
            '       "hazard_title": "Short title of violation",\n'
            '       "observation": "Specific visual evidence in the image",\n'
            '       "haccp_code": "FDA Food Code or HACCP standard reference",\n'
            '       "corrective_action": "Immediate corrective protocol"\n'
            '     }\n'
            '  ],\n'
            '  "auditor_summary": "Comprehensive regulatory summary and passing/failing recommendation."\n'
            "}\n"
            "Compliance score is an integer between 0 and 100. Deduct 25+ points for Critical hazards like raw meat cross-contamination."
        )

        user_content = f"Perform a HACCP hygiene inspection on this kitchen. Environment type: {facility_type}."

        try:
            return self._call_multimodal_vision(image_input, system_prompt, user_content)
        except Exception as e:
            logger.error(f"Error calling AI vision for hygiene: {e}")
            return DEMO_HYGIENE_INSPECTIONS["Commercial Prep Kitchen - Critical Violation"]

    # ==========================================
    # TAB 4: SMART KITCHEN RECIPE ASSISTANT
    # ==========================================
    def generate_recipes(
        self,
        pantry_items: List[str],
        dietary_preference: Optional[str] = "Any",
        meal_type: Optional[str] = "Dinner",
        max_time_mins: int = 40,
        skill_level: str = "Intermediate"
    ) -> List[Dict[str, Any]]:
        """
        Generates creative, nutritious recipes based on user pantry inventory.
        """
        if self.provider == "demo" or not self.client:
            return DEMO_RECIPES

        pantry_str = ", ".join(pantry_items) if pantry_items else "Chicken breast, broccoli, olive oil, garlic"
        system_prompt = (
            "You are Food Verse AI, an executive master chef and nutrition scientist. "
            "Create 2 distinct, highly creative, appetizing recipes utilizing the user's available pantry ingredients. "
            "Respond ONLY with a valid JSON array of recipe objects matching this schema:\n"
            "[\n"
            "  {\n"
            '    "title": "Creative Dish Title",\n'
            '    "cuisine": "Culinary Style",\n'
            '    "prep_time": "15 mins",\n'
            '    "cook_time": "20 mins",\n'
            '    "total_time": "35 mins",\n'
            '    "servings": 2,\n'
            '    "difficulty": "Easy" OR "Intermediate" OR "Master Chef",\n'
            '    "calories_per_serving": 450,\n'
            '    "macros": {"protein": "38g", "carbs": "40g", "fat": "15g", "fiber": "6g"},\n'
            '    "pantry_used": ["ingredient1", "ingredient2"],\n'
            '    "substitutions": ["Ingredient A -> Alternative B if missing"],\n'
            '    "instructions": ["Step 1 detailed action", "Step 2 detailed action"],\n'
            '    "chef_pro_tip": "Insider culinary technique",\n'
            '    "zero_waste_tip": "How to utilize peels, scraps, or leftovers"\n'
            "  }\n"
            "]"
        )

        user_content = (
            f"Available Pantry Inventory: {pantry_str}.\n"
            f"Dietary Constraint: {dietary_preference}.\n"
            f"Meal Type: {meal_type}.\n"
            f"Max Total Cooking Time: {max_time_mins} minutes.\n"
            f"Chef Skill Level: {skill_level}."
        )

        try:
            res_text = self._call_text_llm(system_prompt, user_content)
            parsed = parse_json_from_response(res_text)
            if isinstance(parsed, list) and len(parsed) > 0:
                return parsed
            elif isinstance(parsed, dict) and "recipes" in parsed:
                return parsed["recipes"]
            return DEMO_RECIPES
        except Exception as e:
            logger.error(f"Recipe generation error: {e}")
            return DEMO_RECIPES

    # ==========================================
    # TAB 5: PERSONALIZED MEAL PLANNER
    # ==========================================
    def generate_meal_plan(
        self,
        profile: Dict[str, Any],
        bmr: float,
        tdee: float,
        target_kcal: int,
        macro_targets: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Generates an adaptive 7-day meal schedule + automated categorized grocery list.
        """
        if self.provider == "demo" or not self.client:
            return self._generate_mock_meal_plan(profile, target_kcal, macro_targets)

        system_prompt = (
            "You are Food Verse AI, an elite Clinical Dietitian and Sports Nutritionist. "
            "Formulate an adaptive 7-day meal schedule (Monday through Sunday) with breakfast, lunch, dinner, "
            "and snack, precisely meeting the user's daily caloric target and dietary goals. "
            "Also generate a categorized grocery shopping list for the entire week. "
            "Respond ONLY with a valid JSON object matching this schema:\n"
            "{\n"
            '  "daily_target_calories": 2100,\n'
            '  "dietary_approach": "Description of dietary regime",\n'
            '  "daily_schedule": {\n'
            '     "Monday": {\n'
            '        "calories": 2080,\n'
            '        "breakfast": "Oatmeal with berries & protein whey (450 kcal)",\n'
            '        "lunch": "Grilled chicken quinoa bowl with avocado (650 kcal)",\n'
            '        "dinner": "Baked salmon with roasted asparagus & sweet potato (700 kcal)",\n'
            '        "snack": "Greek yogurt with crushed almonds (280 kcal)"\n'
            '     }\n'
            '     ... include Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday ...\n'
            '  },\n'
            '  "grocery_list": {\n'
            '     "Fresh Produce": ["Baby spinach (500g)", "Avocados (4 units)", ...],\n'
            '     "Proteins & Fish": ["Wild salmon fillets (4x150g)", "Chicken breasts (1kg)", ...],\n'
            '     "Grains & Bakery": ["Organic quinoa (500g)", "Rolled oats (1kg)", ...],\n'
            '     "Dairy & Refrigerated": ["Non-fat Greek yogurt (1kg)", "Eggs (1 dozen)", ...],\n'
            '     "Pantry & Spices": ["Extra virgin olive oil", "Raw almonds", "Sea salt"]\n'
            '  },\n'
            '  "dietitian_coaching_notes": "Key behavioral guidance and meal prep batching strategies."\n'
            "}"
        )

        user_content = (
            f"User Profile: Age {profile.get('age')}, Gender {profile.get('gender')}, "
            f"Weight {profile.get('weight_kg')} kg, Activity {profile.get('activity_level')}, "
            f"Diet: {profile.get('dietary_constraint')}, Goal: {profile.get('fitness_goal')}.\n"
            f"Calculated BMR: {int(bmr)} kcal, TDEE: {int(tdee)} kcal.\n"
            f"Daily Caloric Target: {target_kcal} kcal.\n"
            f"Daily Target Macros: Protein {macro_targets['protein']}g, Carbs {macro_targets['carbs']}g, Fats {macro_targets['fats']}g."
        )

        try:
            res_text = self._call_text_llm(system_prompt, user_content)
            parsed = parse_json_from_response(res_text)
            if isinstance(parsed, dict) and "daily_schedule" in parsed:
                return parsed
            return self._generate_mock_meal_plan(profile, target_kcal, macro_targets)
        except Exception as e:
            logger.error(f"Meal plan generation error: {e}")
            return self._generate_mock_meal_plan(profile, target_kcal, macro_targets)

    def _generate_mock_meal_plan(
        self,
        profile: Dict[str, Any],
        target_kcal: int,
        macro_targets: Dict[str, int]
    ) -> Dict[str, Any]:
        """High quality mock meal plan generator adhering to target kcal."""
        diet = profile.get("dietary_constraint", "Balanced")
        goal = profile.get("fitness_goal", "Lean Recomposition")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sample_meals = [
            ("Protein Berry Oatmeal Bowl with Chia Seeds", "Grilled Herb Chicken Breast with Quinoa & Steamed Broccoli", "Pan-Seared Wild Salmon with Roasted Sweet Potatoes & Asparagus", "Greek Yogurt with Crushed Walnuts & Honey"),
            ("Avocado & Scrambled Egg Sourdough Toast", "Mediterranean Tuna Salad with Olive Oil & Garbanzo Beans", "Lean Turkey Bolognese over High-Protein Lentil Pasta", "Whey Protein Shake with Green Apple"),
            ("Spinach, Banana & Plant Protein Super-Smoothie", "Warm Grass-Fed Beef & Brown Basmati Rice Bowl", "Baked Lemon Cod with Herb Roasted Cauliflower & Baby Potatoes", "Cottage Cheese with Sliced Cucumber & Pumpkin Seeds"),
            ("Fluffy Egg White & Vegetable Omelet with Avocado", "Tofu & Edamame Garlic Ginger Stir-Fry over Brown Rice", "Grilled Marinated Chicken Breast with Baked Yam & Zucchini", "Dark Chocolate Rice Cake with Almond Butter"),
            ("Greek Yogurt Parfait with Mixed Berries & Hemp Seeds", "Wild Salmon Poke Bowl with Seaweed, Avocado & Brown Rice", "Herb-Crusted Flank Steak with Chimichurri & Roasted Carrots", "Hard-Boiled Pasture Eggs with Carrot Sticks"),
            ("Whole Grain Blueberry Protein Waffles with Pure Maple", "Grilled Turkey Burger on Brioche with Mixed Green Salad", "Pan-Seared Sea Bass with Lemon Garlic Quinoa & Green Beans", "Mixed Raw Nuts (Almonds, Cashews, Walnuts)"),
            ("Poached Eggs over Wilted Spinach & Whole Wheat Toast", "Hearty Moroccan Chickpea & Vegetable Tagine Stew", "Slow-Roasted Herb Chicken with Sautéed Kale & Baked Red Potatoes", "Low-Fat Kefir with Cinnamon & Chia Seeds")
        ]

        daily_schedule = {}
        for idx, day in enumerate(days):
            b, l, d, s = sample_meals[idx]
            # Calorie splits approx 25% B, 35% L, 30% D, 10% S
            b_c = int(target_kcal * 0.25)
            l_c = int(target_kcal * 0.35)
            d_c = int(target_kcal * 0.30)
            s_c = target_kcal - (b_c + l_c + d_c)

            daily_schedule[day] = {
                "calories": target_kcal,
                "breakfast": f"{b} (~{b_c} kcal)",
                "lunch": f"{l} (~{l_c} kcal)",
                "dinner": f"{d} (~{d_c} kcal)",
                "snack": f"{s} (~{s_c} kcal)"
            }

        return {
            "daily_target_calories": target_kcal,
            "dietary_approach": f"{diet} Diet optimized for {goal}",
            "daily_schedule": daily_schedule,
            "grocery_list": {
                "Fresh Produce": [
                    "Baby spinach & organic mixed greens (2 large boxes)",
                    "Fresh avocados (5-6 ripe units)",
                    "Broccoli florets (2 heads) & asparagus bunch",
                    "Sweet potatoes / yams (1.5 kg)",
                    "Fresh lemons, garlic bulb, fresh ginger root",
                    "Organic blueberries & strawberries (3 clamshells)"
                ],
                "Proteins & Fish": [
                    "Wild Alaskan salmon fillets (4x160g)",
                    "Boneless skinless chicken breasts (1.5 kg)",
                    "Lean ground turkey or flank steak (600g)",
                    "Extra-firm organic tofu or lentils (2 packs)",
                    "Pasture-raised eggs (2 dozen)"
                ],
                "Grains & Bakery": [
                    "Tri-color organic quinoa (500g)",
                    "Brown basmati or jasmine rice (1kg)",
                    "Rolled whole-grain oats (1kg)",
                    "Fermented artisanal sourdough bread (1 loaf)"
                ],
                "Dairy & Plant-Based": [
                    "0% Greek strained yogurt (1kg tub)",
                    "Low-fat cottage cheese or unsweetened almond milk",
                    "Aged Parmesan or feta block (200g)"
                ],
                "Pantry & Spices": [
                    "Cold-pressed Extra Virgin Olive Oil (500ml)",
                    "Raw unsalted almonds & walnuts (300g)",
                    "Organic chia seeds & hemp hearts",
                    "Low-sodium tamari soy sauce & dried oregano"
                ]
            },
            "dietitian_coaching_notes": (
                "Batch cook your quinoa and brown rice on Sunday evening. Pre-grill chicken breasts and store in "
                "airtight glass meal prep containers for zero friction lunches during busy weekdays."
            )
        }

    # ==========================================
    # INTERNAL MULTIMODAL & TEXT RUNNERS
    # ==========================================
    def _call_multimodal_vision(self, image_input: Any, system_prompt: str, user_content: str) -> Dict[str, Any]:
        """Dispatches multimodal vision request to Gemini or Groq."""
        if self.provider == "gemini":
            return self._call_gemini_vision(image_input, system_prompt, user_content)
        elif self.provider == "groq":
            return self._call_groq_vision(image_input, system_prompt, user_content)
        raise ValueError(f"Unsupported provider: {self.provider}")

    def _call_gemini_vision(self, image_input: Any, system_prompt: str, user_content: str) -> Dict[str, Any]:
        """Calls Gemini Vision API."""
        # Convert image to PIL
        pil_img = None
        if isinstance(image_input, Image.Image):
            pil_img = image_input
        elif hasattr(image_input, "getvalue"):
            pil_img = Image.open(image_input)
        elif isinstance(image_input, (bytes, bytearray)):
            pil_img = Image.open(io.BytesIO(image_input))

        model_name = self.model_name or "gemini-2.5-flash"

        if getattr(self, "_gemini_sdk", "") == "genai":
            response = self.client.models.generate_content(
                model=model_name,
                contents=[system_prompt, user_content, pil_img]
            )
            raw_text = response.text
        else:
            # Legacy SDK
            model = self.client.GenerativeModel(model_name)
            response = model.generate_content([system_prompt, user_content, pil_img])
            raw_text = response.text

        return parse_json_from_response(raw_text)

    def _call_groq_vision(self, image_input: Any, system_prompt: str, user_content: str) -> Dict[str, Any]:
        """Calls Groq Vision API using base64 image encoding."""
        b64 = image_to_base64(image_input)
        model_name = self.model_name or "llama-3.2-11b-vision-preview"

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_content},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    }
                ]
            }
        ]
        completion = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            response_format={"type": "json_object"} if "llama-3.3" in model_name else None
        )
        raw_text = completion.choices[0].message.content
        return parse_json_from_response(raw_text)

    def _call_text_llm(self, system_prompt: str, user_content: str) -> str:
        """Dispatches text-only prompts to Gemini or Groq."""
        if self.provider == "gemini":
            model_name = self.model_name or "gemini-2.5-flash"
            if getattr(self, "_gemini_sdk", "") == "genai":
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=[system_prompt, user_content]
                )
                return response.text
            else:
                model = self.client.GenerativeModel(model_name)
                response = model.generate_content([system_prompt, user_content])
                return response.text
        elif self.provider == "groq":
            model_name = self.model_name or "llama-3.3-70b-versatile"
            completion = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            return completion.choices[0].message.content
        return ""
