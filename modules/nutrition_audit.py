"""
Tab 1: Food Recognition & Nutrition Audit (Epic 2)
Multimodal recognition, macro/micro breakdown, health score calculation,
interactive charts, and allergen safety alerts.
"""

import json
import streamlit as st
from PIL import Image

from utils.charts import create_macro_donut_chart, create_score_gauge
from utils.helpers import get_health_score_badge
from modules.demo_data import DEMO_NUTRITION_ITEMS

def render_nutrition_audit_tab(ai_service):
    st.markdown("""
        <div class="glass-card glass-card-accent">
            <div class="card-header-title">
                🥗 Food Recognition & Nutritional Audit (Epic 2)
            </div>
            <p style="color: #9CA3AF; margin-bottom: 0;">
                Deploy multimodal vision AI to instantly identify dishes, quantify individual ingredients, 
                compute full macronutrient splits, detect allergens, and evaluate clinical health scores.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_display = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("##### 📸 Step 1: Provide Meal Imagery")
        
        input_mode = st.radio(
            "Image Input Mode:",
            ["Choose Curated Demo Dish Preset", "Upload Custom Photo"],
            horizontal=True,
            key="nutri_input_mode"
        )

        selected_image = None
        dish_hint = ""
        portion_hint = ""

        if input_mode == "Choose Curated Demo Dish Preset":
            preset_choice = st.selectbox(
                "Select a Curated Culinary Dish:",
                list(DEMO_NUTRITION_ITEMS.keys()),
                key="nutri_preset_select"
            )
            dish_hint = preset_choice
            st.info(f"Selected: **{preset_choice}** (Click 'Run Multimodal Nutrition Audit' below)")
        else:
            uploaded_file = st.file_uploader(
                "Upload Meal Image (JPG, PNG, WEBP):",
                type=["jpg", "jpeg", "png", "webp"],
                key="nutri_file_uploader"
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)
                st.image(selected_image, caption="Uploaded Meal Photo", use_container_width=True)
            
            dish_hint = st.text_input("Optional Dish Name / Context Hint:", placeholder="e.g. Grilled salmon bowl, chicken curry")
            portion_hint = st.text_input("Optional Portion Size Hint:", placeholder="e.g. 1 standard bowl, 350g, 2 slices")

        run_audit = st.button("🔬 Run Multimodal Nutrition Audit", type="primary", use_container_width=True, key="btn_run_nutrition")

    with col_display:
        st.markdown("##### 📊 Step 2: Multimodal Nutrition Intelligence")
        
        # Check session state for cached result or trigger new audit
        result_key = "cached_nutrition_audit_result"

        if run_audit:
            with st.spinner("Analyzing culinary composition, calculating bio-available macros & allergens..."):
                target_img = selected_image or dish_hint
                result = ai_service.analyze_nutrition(
                    image_input=target_img,
                    dish_name_hint=dish_hint,
                    portion_hint=portion_hint
                )
                st.session_state[result_key] = result
        
        # Render if results exist in session_state
        if result_key in st.session_state:
            res = st.session_state[result_key]
            
            dish_name = res.get("dish_name", "Identified Dish")
            cuisine = res.get("cuisine", "Global Cuisine")
            portion = res.get("portion_size", "Single Serving")
            health_score = int(res.get("health_score", 75))
            cals = res.get("calories_kcal", 0)
            protein = res.get("protein_g", 0.0)
            carbs = res.get("carbohydrates_g", 0.0)
            fats = res.get("fats_g", 0.0)
            fiber = res.get("fiber_g", 0.0)
            sugar = res.get("sugar_g", 0.0)
            sodium = res.get("sodium_mg", 0)

            badge_label, badge_class, _ = get_health_score_badge(health_score)

            # Dish title header
            st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <h3 style="margin: 0; color: #10B981; font-size: 1.4rem;">{dish_name}</h3>
                    <div style="color: #9CA3AF; font-size: 0.9rem; margin-top: 4px;">
                        <span>🌍 <b>Cuisine:</b> {cuisine}</span> &nbsp;|&nbsp; 
                        <span>⚖️ <b>Estimated Portion:</b> {portion}</span>
                    </div>
                    <div class="badge-row">
                        <span class="pill-badge {badge_class}">⭐ {badge_label} ({health_score}/100)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Metric Cards Row
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Energy</div>
                        <div class="metric-value">{cals}</div>
                        <div class="metric-sub">kcal</div>
                    </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Protein</div>
                        <div class="metric-value" style="color: #34D399;">{protein}g</div>
                        <div class="metric-sub">{int(protein * 4)} kcal</div>
                    </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Carbs</div>
                        <div class="metric-value" style="color: #60A5FA;">{carbs}g</div>
                        <div class="metric-sub">{int(carbs * 4)} kcal</div>
                    </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Fats</div>
                        <div class="metric-value" style="color: #FBBF24;">{fats}g</div>
                        <div class="metric-sub">{int(fats * 9)} kcal</div>
                    </div>
                """, unsafe_allow_html=True)

            # Secondary micro metrics
            sm1, sm2, sm3 = st.columns(3)
            with sm1:
                st.markdown(f"<p style='color:#9CA3AF; margin: 8px 0 0 0; font-size:0.85rem;'>🌾 <b>Fiber:</b> {fiber}g</p>", unsafe_allow_html=True)
            with sm2:
                st.markdown(f"<p style='color:#9CA3AF; margin: 8px 0 0 0; font-size:0.85rem;'>🍯 <b>Sugars:</b> {sugar}g</p>", unsafe_allow_html=True)
            with sm3:
                st.markdown(f"<p style='color:#9CA3AF; margin: 8px 0 0 0; font-size:0.85rem;'>🧂 <b>Sodium:</b> {sodium}mg</p>", unsafe_allow_html=True)

            # Visualizations row: Donut chart + Health Score Gauge
            c_donut, c_gauge = st.columns([1.1, 0.9])
            with c_donut:
                st.plotly_chart(create_macro_donut_chart(protein, carbs, fats), use_container_width=True)
            with c_gauge:
                st.plotly_chart(create_score_gauge(health_score, "Composite Health Score"), use_container_width=True)

            # Allergen Alerts Callout
            allergens = res.get("allergen_alerts", [])
            if allergens:
                st.markdown("""
                    <div style="background: rgba(239, 68, 68, 0.12); border-left: 4px solid #EF4444; padding: 10px 14px; border-radius: 8px; margin: 10px 0;">
                        <span style="color: #F87171; font-weight: 700;">⚠️ Potential Allergen Alerts:</span>
                        <span style="color: #FCA5A5; font-size: 0.9rem;"> {}</span>
                    </div>
                """.format(", ".join(allergens)), unsafe_allow_html=True)

            # Dietary flags
            flags = res.get("dietary_flags", [])
            if flags:
                flag_html = " ".join([f"<span class='pill-badge badge-emerald'>✓ {f}</span>" for f in flags])
                st.markdown(f"<div class='badge-row' style='margin-bottom: 12px;'>{flag_html}</div>", unsafe_allow_html=True)

            # Ingredients Breakdown Accordion
            ingredients = res.get("ingredients", [])
            if ingredients:
                with st.expander("📋 Itemized Ingredients & Portion Weights", expanded=False):
                    for ing in ingredients:
                        st.markdown(f"- **{ing.get('name', 'Item')}**: ~{ing.get('weight_g', 0)}g (approx. {ing.get('calories', 0)} kcal)")

            # Dietitian Notes
            st.markdown(f"""
                <div class="glass-card" style="margin-top: 14px;">
                    <div style="font-weight: 700; color: #10B981; font-size: 0.95rem; margin-bottom: 4px;">
                        🩺 Clinical Dietitian & Food Science Analysis:
                    </div>
                    <p style="color: #D1D5DB; font-size: 0.9rem; line-height: 1.5; margin-bottom: 8px;">
                        {res.get('dietitian_review', 'Balanced nutritional profile with adequate micronutrient distribution.')}
                    </p>
                    <div style="font-weight: 600; color: #F59E0B; font-size: 0.85rem;">
                        💡 Optimization Secret: <span style="color: #E5E7EB; font-weight: 400;">{res.get('optimization_tip', 'Incorporate raw leafy greens.')}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Export Audit Report
            st.download_button(
                "📥 Export Full Nutrition Audit (JSON)",
                data=json.dumps(res, indent=2),
                file_name=f"nutrition_audit_{dish_name.lower().replace(' ', '_')}.json",
                mime="application/json",
                key="dl_nutri_json"
            )
        else:
            st.info("👈 Select a curated preset or upload an image, then click 'Run Multimodal Nutrition Audit' to generate insights.")
