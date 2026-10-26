# 🥗 Food Verse AI — Multimodal Food Intelligence Agent
### Skill Wallet Capstone Project 3

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Zero External DB](https://img.shields.io/badge/Database-Zero%20External%20Dependencies-brightgreen.svg)](#)

---

## 🌟 Executive Summary

**Food Verse AI** is an advanced multimodal artificial intelligence system engineered at the intersection of **Computer Vision**, **Clinical Dietetics**, **HACCP Food Safety Regulation**, and **Computational Bioenergetics**.

Designed as **Skill Wallet Capstone Project 3**, the system acts as an autonomous digital food scientist, clinical nutritionist, master chef, and public health hygiene inspector. Built on top of Streamlit with zero external database dependencies, it offers seamless 1-click deployment on **Streamlit Community Cloud** with native support for **Google Gemini**, **Groq Cloud**, and a 100% offline **Standalone Demonstration Fallback Mode**.

---

## 🏛️ Core Intelligence Pillars & Modules

### 🥗 1. Food Recognition & Nutrition Audit (Epic 2)
- **Multimodal Visual Deconstruction:** Analyzes meal photography to classify dishes, culinary tradition, portion weights, and component ingredients.
- **Precision Macronutrient Breakdown:** Calculates Calories (kcal), Protein (g), Carbohydrates (g), Fats (g), Dietary Fiber (g), Free Sugars (g), and Sodium (mg).
- **Composite Health Score (1-100):** Evaluates nutrient density, ultra-processing index, and fiber-to-sugar ratios with clinical rating badges (*Optimal Superfood*, *Nutrient Dense*, *Moderate Balance*, *Indulgent*).
- **Interactive Visualizations:** High-contrast Plotly Donut Charts and Radial Health Gauges.
- **Allergen Detection Matrix:** Instant alerts for Gluten, Dairy, Tree Nuts, Peanuts, Shellfish, Eggs, Sesame, and Soy.

### 🔬 2. Food Freshness & Spoilage Diagnostic (Epic 3)
- **Perishable Visual Pathology:** Inspects raw produce, meats, poultry, dairy, and bakery items.
- **Surface Biomarker Assessment:**
  - *Micro-texture:* Firmness, turgor loss, softening, mucilage/slime.
  - *Discoloration:* Enzymatic oxidation, chlorosis, anthocyanin degradation.
  - *Wrinkling:* Epidermal transpiration and cellular shrinkage.
  - *Pathogen Sporulation:* Early-stage *Botrytis cinerea*, fungal mycelium, bacterial colonies.
- **Freshness Stage Classification:** `[Fresh | Moderately Fresh | Spoiled]` with real-time Freshness Index (0-100%).
- **Actionable Safety Directives:**
  - `Safe to consume`
  - `Consume within 24h` (with culinary salvage guidance)
  - `Discard immediately` (biological pathogen hazard)
- **Post-Harvest Preservation:** Optimal storage temperatures, relative humidity, container ventilation, and ethylene isolation.

### 🧼 3. Kitchen Hygiene & Food Safety Compliance (Epic 4)
- **HACCP & FDA Food Code Computer Vision:** Audits domestic and commercial culinary environments.
- **Key Inspection Indicators:**
  - *Chef Hat & Hair Restraint:* PPE compliance for hairnets and beard restraints.
  - *Glove & Hand Hygiene:* Single-use glove usage and bare-hand contact violations.
  - *Surface Sanitization:* Stainless steel counter cleanliness and quat sanitizer standards.
  - *Cross-Contamination Hazards:* Identifies critical hazards like raw poultry stored or cut adjacent to ready-to-eat produce.
- **Overall Hygiene Compliance Score (%):** Automatic Grade assignment (*Grade A+*, *Grade A*, *Grade B*, *Critical Fail*).
- **Itemized Violation Logs:** Categorized by severity (*Critical*, *Major*, *Minor*) with standard references (e.g., FDA Food Code 3-302.11) and corrective action plans.

### 🍳 4. Smart Kitchen Recipe Assistant (Epic 4)
- **Dynamic Pantry Inventory:** Input available pantry ingredients via quick-load baskets, multi-select tags, or freeform text.
- **Gourmet Recipe Synthesis:** Formulates chef-curated meals complete with prep time, cooking time, servings, and difficulty level.
- **Flexible Substitution Matrix:** Real-time alternatives for missing ingredients (e.g. Tamari for Soy Sauce, Cauliflower Rice for Basmati).
- **Step-by-Step Chef Execution:** Sequenced culinary procedures with insider tips.
- **Zero-Waste Sustainability Hacks:** Creative culinary repurposing of vegetable peels, stems, and leftover trimmings.

### 📅 5. Personalized 7-Day Meal Planner (Epic 5)
- **Clinical Bioenergetics Engine:**
  - Computes Basal Metabolic Rate (**BMR**) via the **Mifflin-St Jeor Equation**:
    $$\text{BMR}_{\text{Male}} = 10 \times \text{wt (kg)} + 6.25 \times \text{ht (cm)} - 5 \times \text{age} + 5$$
    $$\text{BMR}_{\text{Female}} = 10 \times \text{wt (kg)} + 6.25 \times \text{ht (cm)} - 5 \times \text{age} - 161$$
  - Total Daily Energy Expenditure (**TDEE**) adjusted for physical activity multipliers.
  - Adaptive Caloric Targets: Deficit (-450 kcal) for Fat Loss, Surplus (+350 kcal) for Muscle Hypertrophy.
- **Adaptive 7-Day Meal Schedule:** Monday through Sunday breakdown for Breakfast, Lunch, Dinner, and Energy Snacks.
- **Synchronized Grocery Checklist:** Automatically grouped by supermarket department (*Fresh Produce*, *Butcher & Fishmonger*, *Grains & Bakery*, *Dairy & Plant-Based*, *Pantry & Spices*).

---

## 🛠️ Technology Stack & Architecture

```
skill-wallet/
├── app.py                      # Main Streamlit Application entrypoint & UI routing
├── requirements.txt            # Minimal dependencies for Streamlit Cloud
├── test_app.py                 # Automated unit and integration test suite
├── README.md                   # Complete architectural documentation
├── .streamlit/
│   ├── config.toml             # Custom emerald dark theme configuration
│   └── credentials.toml        # Headless credentials bypass
├── modules/
│   ├── __init__.py
│   ├── ai_service.py           # Unified Multimodal Provider (Gemini, Groq, Demo fallback)
│   ├── nutrition_audit.py      # Tab 1: Food Recognition & Macro Breakdown
│   ├── freshness_diagnostic.py # Tab 2: Perishable Spoilage Diagnostic
│   ├── hygiene_compliance.py   # Tab 3: Kitchen Hygiene & HACCP Auditing
│   ├── recipe_assistant.py     # Tab 4: Pantry Inventory to Recipe Engine
│   ├── meal_planner.py         # Tab 5: BMR/TDEE & 7-Day Meal Scheduler
│   └── demo_data.py            # Rich standalone demonstration presets
└── utils/
    ├── __init__.py
    ├── charts.py               # Plotly interactive charts & gauges
    ├── styles.py               # Custom CSS glassmorphism and color badges
    └── helpers.py              # Base64 converters, JSON repair, export utilities
```

---

## 🚀 Quick Start & Local Execution

### 1. Clone or Navigate to Directory
```bash
cd "skill wallet"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure API Keys
You can run the app immediately in **Standalone Showcase Mode** without any API key.
Alternatively, create a `.env` file or export your keys:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
# or
export GROQ_API_KEY="your-groq-api-key"
```

### 4. Run Automated Test Suite
```bash
python test_app.py
```

### 5. Launch Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 1-Click Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and click **"New app"**.
3. Select your repository, branch, and specify `app.py` as the Main file path.
4. (Optional) In the App Settings under **Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
5. Click **Deploy!** The application will be live globally in under 60 seconds.

---

## 📄 License & Attribution
Developed as **Capstone Project 3** for the **Skill Wallet** AI Engineering curriculum.
Licensed under the [MIT License](LICENSE).
