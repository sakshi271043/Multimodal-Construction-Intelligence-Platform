"""
High-fidelity standalone demonstration datasets and presets for Food Verse AI.
Allows 100% full-featured demonstration without requiring external API keys.
"""

from typing import Dict, Any, List

DEMO_NUTRITION_ITEMS: Dict[str, Dict[str, Any]] = {
    "Mediterranean Salmon & Quinoa Bowl": {
        "dish_name": "Mediterranean Wild Salmon & Quinoa Superbowl",
        "cuisine": "Mediterranean / Healthy Coastal",
        "portion_size": "1 large bowl (approx. 420g)",
        "calories_kcal": 560,
        "protein_g": 38.5,
        "carbohydrates_g": 44.0,
        "fats_g": 22.0,
        "fiber_g": 9.2,
        "sugar_g": 4.5,
        "sodium_mg": 480,
        "health_score": 94,
        "dietary_flags": ["Pescatarian", "High Protein", "Heart Healthy", "Gluten-Free Friendly"],
        "allergen_alerts": ["Fish (Salmon)", "May contain traces of sesame"],
        "ingredients": [
            {"name": "Wild Alaskan Salmon Fillet (Pan-seared)", "weight_g": 160, "calories": 280},
            {"name": "Fluffy Tri-Color Quinoa", "weight_g": 120, "calories": 145},
            {"name": "Hass Avocado Slices", "weight_g": 50, "calories": 80},
            {"name": "Baby Spinach & Cucumber Ribbons", "weight_g": 60, "calories": 15},
            {"name": "Extra Virgin Olive Oil & Lemon Dressing", "weight_g": 20, "calories": 110},
            {"name": "Toasted Pumpkin Seeds", "weight_g": 10, "calories": 55}
        ],
        "dietitian_review": (
            "Outstanding nutritional density. High in anti-inflammatory EPA/DHA Omega-3 fatty acids from wild salmon, "
            "complete amino acid profile from quinoa, and rich in monounsaturated fats from avocado. "
            "Exceeds 30% of daily fiber requirements with minimal glycemic impact."
        ),
        "optimization_tip": "Add a sprinkle of fermented sauerkraut or kefir dressing to elevate gut microbiome biodiversity."
    },
    "Authentic Chicken Tikka Masala with Garlic Naan": {
        "dish_name": "Tandoori Chicken Tikka Masala with Butter Garlic Naan",
        "cuisine": "North Indian / Mughlai",
        "portion_size": "1 entree plate (approx. 480g)",
        "calories_kcal": 820,
        "protein_g": 46.0,
        "carbohydrates_g": 72.0,
        "fats_g": 38.0,
        "fiber_g": 5.4,
        "sugar_g": 9.0,
        "sodium_mg": 920,
        "health_score": 68,
        "dietary_flags": ["High Protein", "Non-Vegetarian"],
        "allergen_alerts": ["Dairy (Cream, Ghee, Yogurt)", "Gluten (Wheat Naan)", "Cashew/Nut paste"],
        "ingredients": [
            {"name": "Tandoori Marinated Chicken Breast", "weight_g": 180, "calories": 260},
            {"name": "Spiced Tomato-Cream Masala Gravy", "weight_g": 150, "calories": 250},
            {"name": "Clay-Oven Baked Garlic Naan", "weight_g": 110, "calories": 270},
            {"name": "Ghee & Cilantro Garnish", "weight_g": 10, "calories": 90}
        ],
        "dietitian_review": (
            "Substantial protein source with active bioavailability from tandoori chicken. "
            "Rich in bioactive curcumin and capsaicin from spices. However, the meal contains significant "
            "saturated fats from heavy cream and refined carbohydrates from white flour naan."
        ),
        "optimization_tip": "Swap the refined naan for whole wheat tandoori roti and substitute half the heavy cream with Greek yogurt to shave 210 kcal and reduce saturated fat by 40%."
    },
    "Avocado Toast with Poached Egg & Microgreens": {
        "dish_name": "Artisanal Sourdough Avocado Toast with Poached Organic Egg",
        "cuisine": "Contemporary Californian / Brunch",
        "portion_size": "2 open slices (approx. 270g)",
        "calories_kcal": 440,
        "protein_g": 19.5,
        "carbohydrates_g": 36.0,
        "fats_g": 24.0,
        "fiber_g": 8.0,
        "sugar_g": 2.8,
        "sodium_mg": 410,
        "health_score": 88,
        "dietary_flags": ["Vegetarian", "Whole Food", "Low Glycemic"],
        "allergen_alerts": ["Eggs", "Gluten (Sourdough wheat)"],
        "ingredients": [
            {"name": "Slow-fermented Sourdough Slices", "weight_g": 90, "calories": 190},
            {"name": "Crushed Hass Avocado with Lime", "weight_g": 80, "calories": 130},
            {"name": "Pasture-Raised Poached Eggs", "weight_g": 90, "calories": 120},
            {"name": "Radish Microgreens & Red Pepper Flakes", "weight_g": 10, "calories": 8}
        ],
        "dietitian_review": (
            "Well-balanced nutrient distribution. Natural fermentation in sourdough slows starch absorption, "
            "while the lutein and choline in whole egg yolk support cognitive acuity. Rich in potassium and dietary fiber."
        ),
        "optimization_tip": "Dust with hemp hearts or chia seeds for an effortless +4g plant protein and essential ALA fatty acids."
    },
    "Classic Margherita Pizza Slice": {
        "dish_name": "Neapolitan Margherita Pizza (2 Slices)",
        "cuisine": "Italian / Napoli",
        "portion_size": "2 medium slices (approx. 210g)",
        "calories_kcal": 510,
        "protein_g": 21.0,
        "carbohydrates_g": 58.0,
        "fats_g": 18.0,
        "fiber_g": 3.8,
        "sugar_g": 5.2,
        "sodium_mg": 890,
        "health_score": 62,
        "dietary_flags": ["Vegetarian"],
        "allergen_alerts": ["Dairy (Fresh Mozzarella)", "Gluten (00 Flour)"],
        "ingredients": [
            {"name": "Wood-fired Pizza Crust (Type 00 Flour)", "weight_g": 130, "calories": 310},
            {"name": "San Marzano Tomato Sauce & Fresh Basil", "weight_g": 40, "calories": 35},
            {"name": "Fior di Latte Mozzarella Cheese", "weight_g": 50, "calories": 140},
            {"name": "Cold-Pressed Extra Virgin Olive Oil", "weight_g": 5, "calories": 45}
        ],
        "dietitian_review": (
            "Moderate caloric density with good calcium content from whole mozzarella. San Marzano tomatoes provide "
            "antioxidant lycopene. However, it leans high on glycemic load and sodium per serving."
        ),
        "optimization_tip": "Pair with a crisp arugula side salad dressed in balsamic vinegar to add polyphenol volume and blunt blood glucose spikes."
    }
}

DEMO_FRESHNESS_ITEMS: Dict[str, Dict[str, Any]] = {
    "Fresh Hass Avocado": {
        "item_name": "Hass Avocado (Persea americana)",
        "category": "Fresh Produce / Climacteric Fruit",
        "freshness_stage": "Fresh",
        "freshness_index": 92,
        "surface_evaluation": {
            "texture": "Firm yet gently yielding under thumb pressure; pebbled skin intact with uniform dark emerald hue.",
            "discoloration": "No necrotic brown patches or oxidation visible at stem junction.",
            "wrinkling": "Minimal to zero skin epidermal dehydration.",
            "mold_status": "Zero fungal hyphae or surface mycelium detected."
        },
        "food_safety_advice": "Safe to consume immediately or store for optimal ripeness.",
        "shelf_life_remaining": "3 to 5 days at room temperature (up to 9 days if refrigerated at 4°C).",
        "storage_tips": [
            "Store unpeeled at 15-20°C until soft; once ripe, transfer to the refrigerator vegetable crisper.",
            "Keep away from apples and bananas if you wish to delay ethylene-induced ripening.",
            "If cut open, brush exposed flesh with citrus juice (ascorbic acid) and cover with beeswax wrap to prevent polyphenol oxidase browning."
        ],
        "salvage_tips": "In prime state for salads, fresh guacamole, or sliced on artisanal toast."
    },
    "Overripe Brown Spotted Avocado": {
        "item_name": "Overripe Hass Avocado",
        "category": "Fresh Produce / Climacteric Fruit",
        "freshness_stage": "Moderately Fresh",
        "freshness_index": 58,
        "surface_evaluation": {
            "texture": "Deeply yielding, soft hollow pockets under stem area; loss of epidermal turgor.",
            "discoloration": "Moderate internal enzymatic oxidation (brown vascular strands present in flesh).",
            "wrinkling": "Pronounced epidermal shrinkage around the neck and base.",
            "mold_status": "No external mold spores present, but cellular membrane integrity is compromised."
        },
        "food_safety_advice": "Consume within 24 hours. Excise brown oxidized portions; flesh remains safe if no foul fermented odor.",
        "shelf_life_remaining": "12 to 24 hours maximum before rancidity onset.",
        "storage_tips": [
            "Scoop out remaining green flesh immediately, blend with lemon juice and freeze in silicone ice trays.",
            "Do not leave at room temperature as lipid rancidity accelerates exponentially."
        ],
        "salvage_tips": "Ideal for chocolate avocado pudding, high-fat keto green smoothies, or zero-waste vegan baking fat replacement."
    },
    "Surface Mold Fresh Strawberries": {
        "item_name": "Commercial Fresh Strawberries (Fragaria × ananassa)",
        "category": "Perishable Soft Berry",
        "freshness_stage": "Spoiled",
        "freshness_index": 18,
        "surface_evaluation": {
            "texture": "Extensive tissue softening, collapsed water-soaked achenes, and macerated pulp.",
            "discoloration": "Dull brownish-grey patches replacing natural anthocyanin red gloss.",
            "wrinkling": "Severe moisture transpiration leading to shriveled pericarp.",
            "mold_status": "Critical: Visible Botrytis cinerea (Grey Mold) mycelium and fungal spore fuzz present."
        },
        "food_safety_advice": "Discard immediately. Do not attempt to salvage by cutting around mold; fungal hyphae penetrate porous soft berries completely.",
        "shelf_life_remaining": "0 days - Immediate biological hazard.",
        "storage_tips": [
            "Never wash strawberries prior to storage, as excess surface moisture promotes Botrytis spore germination.",
            "Inspect container and remove any damaged fruit immediately before spores spread to adjoining berries.",
            "Store in a ventilated container lined with paper towels at 1-2°C with 90-95% relative humidity."
        ],
        "salvage_tips": "Do not consume or compost in indoor bins. Safely bag and dispose of in municipal organic waste."
    },
    "Aged Grass-Fed Ribeye Steak": {
        "item_name": "Chilled Beef Ribeye Cut (Bos taurus)",
        "category": "Perishable Fresh Red Meat",
        "freshness_stage": "Fresh",
        "freshness_index": 88,
        "surface_evaluation": {
            "texture": "Firm, springy myofibrillar resilience; clean intramuscular marbling without surface mucilage.",
            "discoloration": "Natural bright cherry-red (oxymyoglobin) on exterior; no greenish or slate-gray tinge.",
            "wrinkling": "Normal surface dry-aging crust formation, no tacky slime film.",
            "mold_status": "Completely free of fungal or bacterial slime colonies."
        },
        "food_safety_advice": "Safe to consume. Cook to internal minimum temperature of 54°C (medium rare) or 63°C per USDA/FDA guidance.",
        "shelf_life_remaining": "3 to 4 days refrigerated below 3°C, or freeze up to 6 months at -18°C.",
        "storage_tips": [
            "Keep in the coldest sector of refrigerator (bottom shelf, rear).",
            "Store in vacuum-sealed bag or butcher paper over a drip tray to prevent moisture pooling.",
            "Never store unsealed near fresh ready-to-eat produce."
        ],
        "salvage_tips": "Perfect for high-heat reverse sear or cast iron skillet cooking."
    }
}

DEMO_HYGIENE_INSPECTIONS: Dict[str, Dict[str, Any]] = {
    "Commercial Prep Kitchen - Critical Violation": {
        "scene_name": "Active Prep Line Inspection - Station 3",
        "facility_type": "Commercial High-Volume Restaurant Kitchen",
        "compliance_score": 58,
        "compliance_grade": "Grade C / Fail (Action Required)",
        "detected_indicators": {
            "hair_restraint_compliance": "Violation (1 of 3 food handlers without hairnet or beard restraint)",
            "glove_ppe_compliance": "Violation (Direct bare-hand contact observed with ready-to-eat sliced tomatoes)",
            "surface_sanitization": "Non-Compliant (Food debris accumulation and unverified chemical quat sanitizer bucket)",
            "cross_contamination_hazard": "Critical Danger: Raw poultry prep board placed directly adjacent to unwashed leafy greens without 24-inch physical separation"
        },
        "violations": [
            {
                "severity": "Critical",
                "hazard_title": "Cross-Contamination - Raw Poultry & Ready-to-Eat Produce",
                "observation": "Yellow cutting board containing raw chicken breast trim placed in direct contact with stainless prep bin containing washed Romaine lettuce.",
                "haccp_code": "FDA Food Code 3-302.11 / HACCP Critical Control Point 2",
                "corrective_action": "Immediately condemn and discard exposed lettuce. Sanitize entire stainless prep table with 200ppm quaternary ammonium solution. Designate red board exclusively for poultry."
            },
            {
                "severity": "Major",
                "hazard_title": "Bare Hand Contact with Ready-to-Eat Food",
                "observation": "Line chef plating sandwich garnishes without single-use nitrile gloves or clean deli tongs.",
                "haccp_code": "FDA Food Code 3-301.11(B)",
                "corrective_action": "Enforce mandatory 20-second warm water handwashing protocol and dispense food-grade disposable gloves prior to re-entering prep zone."
            },
            {
                "severity": "Minor",
                "hazard_title": "Improper Staff Hair Restraints",
                "observation": "Prep staff member operating adjacent to convection oven without approved hairnet or beard net.",
                "haccp_code": "FDA Food Code 2-402.11",
                "corrective_action": "Provide disposable hairnet and beard snood immediately; verify personal hygiene compliance checklist at shift kickoff."
            }
        ],
        "auditor_summary": "Facility failed key biological hazard prevention criteria due to raw meat cross-contact risks. Mandatory retraining and immediate sanitization required prior to dinner service."
    },
    "Michelin Star Certified Prep Kitchen": {
        "scene_name": "Fine Dining Culinary Lab - Cold Larder & Garde Manger",
        "facility_type": "Fine Dining Commercial Kitchen",
        "compliance_score": 96,
        "compliance_grade": "Grade A+ (Exemplary Compliance)",
        "detected_indicators": {
            "hair_restraint_compliance": "100% Compliant (All staff wearing chefs caps and clean white aprons)",
            "glove_ppe_compliance": "100% Compliant (Color-coded food handling gloves in use with frequent rotation)",
            "surface_sanitization": "Pristine (Sanitized 316-grade stainless steel surfaces; labeled sanitizer test strips active)",
            "cross_contamination_hazard": "Zero Hazard (Strict HACCP spatial isolation; independent wash and prep zones)"
        },
        "violations": [
            {
                "severity": "Minor",
                "hazard_title": "Digital Probe Thermometer Log Lag",
                "observation": "Walk-in cooler temperature log was completed 15 minutes past the standard 10:00 AM audit milestone (actual temp: 2.8°C, fully within 1-4°C safety spec).",
                "haccp_code": "HACCP Monitoring CCP 1",
                "corrective_action": "Calibrate automated IoT thermal sensor to ping digital tablet alert 5 minutes prior to shift audit."
            }
        ],
        "auditor_summary": "World-class food hygiene compliance. Impeccable spatial hygiene, cold chain management, and exemplary personnel sanitization protocols."
    }
}

DEMO_RECIPES = [
    {
        "title": "Lemon Herb Pan-Seared Chicken with Quinoa & Steamed Broccoli",
        "cuisine": "Modern Healthy Mediterranean",
        "prep_time": "15 mins",
        "cook_time": "20 mins",
        "total_time": "35 mins",
        "servings": 2,
        "difficulty": "Easy",
        "calories_per_serving": 460,
        "macros": {"protein": "42g", "carbs": "36g", "fat": "14g", "fiber": "7g"},
        "pantry_used": ["Chicken breast", "Broccoli", "Quinoa", "Olive oil", "Garlic", "Lemon"],
        "substitutions": [
            "Chicken breast -> Extra-firm pressed tofu or salmon fillet",
            "Broccoli -> Asparagus spears or snap peas",
            "Quinoa -> Brown basmati rice or farro"
        ],
        "instructions": [
            "Rinse quinoa under cold water. Simmer 1 cup quinoa with 2 cups water and a pinch of sea salt for 14 minutes until fluffy.",
            "Butterfly chicken breasts and pat dry. Season with minced garlic, dried oregano, sea salt, cracked black pepper, and 1 tbsp olive oil.",
            "Sear chicken in a cast-iron skillet over medium-high heat for 5-6 minutes per side until internal temperature hits 74°C (165°F). Finish with fresh lemon juice.",
            "Steam broccoli florets for 4 minutes until vibrant green and tender-crisp.",
            "Plate fluffy quinoa, sliced chicken breast, and broccoli. Drizzle with pan pan-juices and zest of fresh lemon."
        ],
        "chef_pro_tip": "Rest chicken for 4 full minutes on a cutting board before slicing so the flavorful intracellular juices redistribute.",
        "zero_waste_tip": "Do not throw away broccoli stems! Peel the fibrous outer skin, slice into coins, and steam alongside the florets for extra crunchy fiber."
    },
    {
        "title": "Crispy Tofu & Rainbow Vegetable Garlic Ginger Stir-Fry",
        "cuisine": "Asian Fusion / Plant-Based",
        "prep_time": "12 mins",
        "cook_time": "14 mins",
        "total_time": "26 mins",
        "servings": 2,
        "difficulty": "Beginner-Friendly",
        "calories_per_serving": 380,
        "macros": {"protein": "26g", "carbs": "42g", "fat": "12g", "fiber": "8g"},
        "pantry_used": ["Tofu", "Bell pepper", "Broccoli", "Soy sauce", "Garlic", "Ginger", "Brown rice"],
        "substitutions": [
            "Tofu -> Edamame, tempeh, or sliced chicken tenderloins",
            "Soy sauce -> Tamari (Gluten-Free) or Coconut Aminos (Low Sodium)",
            "Brown rice -> Cauliflower rice or soba noodles"
        ],
        "instructions": [
            "Press block of extra-firm tofu with a heavy skillet for 10 minutes to extract excess moisture. Cut into 2cm cubes and toss with 1 tsp cornstarch.",
            "Heat 1 tbsp sesame or avocado oil in a wok. Sear tofu cubes until golden brown and crispy on all sides (6-7 minutes). Transfer to a paper towel.",
            "In the same hot wok, flash-fry minced garlic, grated fresh ginger, sliced bell peppers, and broccoli florets for 3 minutes on high heat.",
            "Whisk 2 tbsp low-sodium soy sauce with 1 tsp rice vinegar and 1 tsp raw honey or maple syrup. Pour sauce into wok to glaze vegetables.",
            "Toss crispy tofu back into wok for 60 seconds to coat. Serve steaming over warm brown rice garnished with toasted sesame seeds."
        ],
        "chef_pro_tip": "A light cornstarch dusting is the secret restaurant technique for glass-like crispy tofu without deep frying.",
        "zero_waste_tip": "Collect bell pepper cores and ginger peels in a freezer bag to steep for aromatic vegetable stock bases."
    }
]
