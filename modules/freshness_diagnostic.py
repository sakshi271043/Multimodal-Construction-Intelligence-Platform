"""
Tab 2: Food Freshness & Spoilage Diagnostic (Epic 3)
Multimodal vision analysis evaluating surface texture, discoloration, wrinkling,
and mold detection to classify freshness stages [Fresh | Moderately Fresh | Spoiled].
"""

import json
import streamlit as st
from PIL import Image

from utils.charts import create_score_gauge
from utils.helpers import get_freshness_badge
from modules.demo_data import DEMO_FRESHNESS_ITEMS

def render_freshness_diagnostic_tab(ai_service):
    st.markdown("""
        <div class="glass-card glass-card-accent">
            <div class="card-header-title">
                🔬 Food Freshness & Spoilage Diagnostic (Epic 3)
            </div>
            <p style="color: #9CA3AF; margin-bottom: 0;">
                Perform computer vision pathology on raw perishables (produce, meats, dairy, bakery).
                Detect cellular breakdown, surface mold spores, moisture loss, and receive actionable food safety guidance.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_display = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("##### 🍎 Step 1: Supply Perishable Food Image")
        
        mode = st.radio(
            "Perishable Selection Mode:",
            ["Choose Curated Perishable Sample", "Upload Custom Perishable Photo"],
            horizontal=True,
            key="fresh_input_mode"
        )

        selected_image = None
        item_hint = ""

        if mode == "Choose Curated Perishable Sample":
            preset_choice = st.selectbox(
                "Select Perishable Specimen:",
                list(DEMO_FRESHNESS_ITEMS.keys()),
                key="fresh_preset_select"
            )
            item_hint = preset_choice
            st.info(f"Selected: **{preset_choice}** (Click 'Run Diagnostic' below)")
        else:
            uploaded_file = st.file_uploader(
                "Upload Perishable Photo (Produce / Meat / Dairy / Bakery):",
                type=["jpg", "jpeg", "png", "webp"],
                key="fresh_file_uploader"
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)
                st.image(selected_image, caption="Uploaded Perishable Item", use_container_width=True)
            item_hint = st.text_input("Optional Item Name / Category:", placeholder="e.g. Hass Avocado, Strawberries, Ground Beef")

        run_diagnostic = st.button("🔎 Run Vision Spoilage Diagnostic", type="primary", use_container_width=True, key="btn_run_freshness")

    with col_display:
        st.markdown("##### 🛡️ Step 2: Freshness Pathology & Safety Verdict")

        result_key = "cached_freshness_diagnostic_result"

        if run_diagnostic:
            with st.spinner("Scanning surface micro-textures, discoloration bands, and fungal sporulation..."):
                target_img = selected_image or item_hint
                result = ai_service.analyze_freshness(
                    image_input=target_img,
                    item_name_hint=item_hint
                )
                st.session_state[result_key] = result

        if result_key in st.session_state:
            res = st.session_state[result_key]

            item_name = res.get("item_name", "Perishable Specimen")
            category = res.get("category", "General Foodstuff")
            stage = res.get("freshness_stage", "Fresh")
            index = int(res.get("freshness_index", 80))
            advice = res.get("food_safety_advice", "Safe to consume.")
            shelf_life = res.get("shelf_life_remaining", "2-3 days")
            surface = res.get("surface_evaluation", {})

            badge_label, badge_class, _ = get_freshness_badge(stage)

            # Freshness Banner
            callout_class = "fresh-callout"
            icon = "✅"
            if "Moderate" in stage:
                callout_class = "moderate-callout"
                icon = "⏳"
            elif "Spoil" in stage:
                callout_class = "spoiled-callout"
                icon = "🛑"

            st.markdown(f"""
                <div class="{callout_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF;">{icon} {stage.upper()}</span>
                            <span style="color: #D1D5DB; margin-left: 8px;">({item_name})</span>
                        </div>
                        <span class="pill-badge {badge_class}">{badge_label}</span>
                    </div>
                    <div style="margin-top: 8px; font-weight: 700; color: #FFFFFF;">
                        Safety Directive: <span style="font-weight: 400; color: #F3F4F6;">{advice}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Metric / Gauge row
            col_g, col_metrics = st.columns([1, 1])
            with col_g:
                st.plotly_chart(create_score_gauge(index, "Freshness Index"), use_container_width=True)
            with col_metrics:
                st.markdown(f"""
                    <div class="metric-card" style="margin-top: 10px;">
                        <div class="metric-label">Estimated Shelf Life</div>
                        <div class="metric-value" style="font-size: 1.3rem; color: #FBBF24;">{shelf_life}</div>
                        <div class="metric-sub">Category: {category}</div>
                    </div>
                """, unsafe_allow_html=True)

            # Itemized Surface Diagnostics Card
            st.markdown("###### 🔍 Surface Pathology Diagnostic Breakdown:")
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.5); padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem;">
                        <b style="color: #60A5FA;">🔬 Surface Texture:</b><br/>
                        <span style="color: #D1D5DB;">{surface.get('texture', 'Standard turgor maintained.')}</span>
                    </div>
                    <div style="background: rgba(31, 41, 55, 0.5); padding: 10px; border-radius: 8px; font-size: 0.85rem;">
                        <b style="color: #FBBF24;">🎨 Discoloration / Oxidation:</b><br/>
                        <span style="color: #D1D5DB;">{surface.get('discoloration', 'No pigment degradation.')}</span>
                    </div>
                """, unsafe_allow_html=True)
            with t_col2:
                st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.5); padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem;">
                        <b style="color: #A78BFA;">💧 Dehydration / Wrinkling:</b><br/>
                        <span style="color: #D1D5DB;">{surface.get('wrinkling', 'Minimal moisture loss.')}</span>
                    </div>
                    <div style="background: rgba(31, 41, 55, 0.5); padding: 10px; border-radius: 8px; font-size: 0.85rem;">
                        <b style="color: #F87171;">🍄 Mold & Pathogens:</b><br/>
                        <span style="color: #D1D5DB;">{surface.get('mold_status', 'No fungal sporulation observed.')}</span>
                    </div>
                """, unsafe_allow_html=True)

            # Preservation Storage Tips
            storage_tips = res.get("storage_tips", [])
            if storage_tips:
                st.markdown("###### 🧊 Food Science Preservation & Storage Guidance:")
                for tip in storage_tips:
                    st.markdown(f"- ❄️ {tip}")

            # Salvage or Disposal Guidance
            salvage = res.get("salvage_tips")
            if salvage:
                st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 3px solid #10B981; padding: 10px 14px; border-radius: 6px; margin-top: 10px; font-size: 0.88rem;">
                        <b style="color: #34D399;">♻️ Zero-Waste Salvage & Culinary Utility:</b><br/>
                        <span style="color: #E5E7EB;">{salvage}</span>
                    </div>
                """, unsafe_allow_html=True)

            # Download Diagnostic
            st.download_button(
                "📥 Export Spoilage Diagnostic (JSON)",
                data=json.dumps(res, indent=2),
                file_name=f"freshness_diagnostic_{item_name.lower().replace(' ', '_')}.json",
                mime="application/json",
                key="dl_fresh_json"
            )
        else:
            st.info("👈 Select a perishable specimen or upload a photo to initiate vision spoilage pathology.")
