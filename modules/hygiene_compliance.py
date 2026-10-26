"""
Tab 3: Kitchen Hygiene & Food Safety Compliance (Epic 4)
Visual safety inspection for commercial and domestic kitchens.
Audits chef hats/hairnets, glove PPE, sanitization state, cross-contamination,
computes overall compliance score (%), and generates itemized violation logs.
"""

import json
import streamlit as st
from PIL import Image

from utils.charts import create_compliance_gauge
from utils.helpers import get_hygiene_score_badge
from modules.demo_data import DEMO_HYGIENE_INSPECTIONS

def render_hygiene_compliance_tab(ai_service):
    st.markdown("""
        <div class="glass-card glass-card-accent">
            <div class="card-header-title">
                🧼 Kitchen Hygiene & Food Safety Compliance (Epic 4)
            </div>
            <p style="color: #9CA3AF; margin-bottom: 0;">
                Automated HACCP & FDA Food Code visual compliance inspection. Detect protective wear violations, 
                sanitization lapses, and cross-contamination hazards (such as raw poultry adjacent to salad prep).
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_display = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("##### 🏢 Step 1: Supply Kitchen Scene")

        mode = st.radio(
            "Inspection Scene Source:",
            ["Choose Curated Kitchen Scenario", "Upload Kitchen Image / Video Frame"],
            horizontal=True,
            key="hygiene_input_mode"
        )

        selected_image = None
        facility_type = "Commercial Kitchen"
        scene_hint = ""

        if mode == "Choose Curated Kitchen Scenario":
            preset_choice = st.selectbox(
                "Select Kitchen Audit Scenario:",
                list(DEMO_HYGIENE_INSPECTIONS.keys()),
                key="hygiene_preset_select"
            )
            scene_hint = preset_choice
            st.info(f"Selected: **{preset_choice}** (Click 'Run Compliance Audit' below)")
        else:
            uploaded_file = st.file_uploader(
                "Upload Kitchen Photo or Video Frame (JPG, PNG, MP4 snapshot):",
                type=["jpg", "jpeg", "png", "webp", "mp4"],
                key="hygiene_file_uploader"
            )
            if uploaded_file:
                if uploaded_file.type.startswith("video"):
                    st.video(uploaded_file)
                    st.caption("Video uploaded. Food Verse AI will audit key active frames.")
                else:
                    selected_image = Image.open(uploaded_file)
                    st.image(selected_image, caption="Uploaded Kitchen Environment", use_container_width=True)

            facility_type = st.selectbox(
                "Facility Classification:",
                ["Commercial Restaurant Kitchen", "Cloud Kitchen / Dark Kitchen", "Institutional / Hospital Foodservice", "Catering & Event Prep", "Domestic Home Kitchen"],
                key="hygiene_facility_select"
            )
            scene_hint = facility_type

        run_audit = st.button("📋 Run HACCP Hygiene Compliance Audit", type="primary", use_container_width=True, key="btn_run_hygiene")

    with col_display:
        st.markdown("##### 📊 Step 2: Regulatory Compliance Audit Results")

        result_key = "cached_hygiene_compliance_result"

        if run_audit:
            with st.spinner("Executing HACCP spatial hazard scans, PPE compliance, and biological cross-contamination checks..."):
                target_img = selected_image or scene_hint
                result = ai_service.audit_kitchen_hygiene(
                    image_input=target_img,
                    facility_type=scene_hint
                )
                st.session_state[result_key] = result

        if result_key in st.session_state:
            res = st.session_state[result_key]

            scene_name = res.get("scene_name", "Inspected Kitchen Line")
            facility = res.get("facility_type", "Commercial Kitchen")
            score = int(res.get("compliance_score", 70))
            grade = res.get("compliance_grade", "Grade B")
            indicators = res.get("detected_indicators", {})
            violations = res.get("violations", [])
            summary = res.get("auditor_summary", "Audit completed.")

            grade_label, grade_badge_class, _ = get_hygiene_score_badge(score)

            # Score Banner
            st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <h3 style="margin:0; color: #FFFFFF; font-size: 1.25rem;">{scene_name}</h3>
                            <span style="color: #9CA3AF; font-size: 0.85rem;">Facility: {facility}</span>
                        </div>
                        <span class="pill-badge {grade_badge_class}">{grade_label}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Gauge Meter
            st.plotly_chart(create_compliance_gauge(score), use_container_width=True)

            # Core Indicators Grid
            st.markdown("###### 🔍 Monitored Hygiene Pillars:")
            p1, p2 = st.columns(2)
            with p1:
                st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.4); padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.82rem;">
                        <b style="color: #38BDF8;">🧢 Hairnet & Beard Restraint:</b><br/>
                        <span style="color: #E5E7EB;">{indicators.get('hair_restraint_compliance', 'Audited')}</span>
                    </div>
                    <div style="background: rgba(31, 41, 55, 0.4); padding: 10px; border-radius: 8px; font-size: 0.82rem;">
                        <b style="color: #34D399;">🧤 Glove & Hand PPE:</b><br/>
                        <span style="color: #E5E7EB;">{indicators.get('glove_ppe_compliance', 'Audited')}</span>
                    </div>
                """, unsafe_allow_html=True)
            with p2:
                st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.4); padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.82rem;">
                        <b style="color: #FBBF24;">🧽 Surface Sanitization:</b><br/>
                        <span style="color: #E5E7EB;">{indicators.get('surface_sanitization', 'Audited')}</span>
                    </div>
                    <div style="background: rgba(31, 41, 55, 0.4); padding: 10px; border-radius: 8px; font-size: 0.82rem;">
                        <b style="color: #F87171;">☣️ Cross-Contamination Risk:</b><br/>
                        <span style="color: #E5E7EB;">{indicators.get('cross_contamination_hazard', 'None detected')}</span>
                    </div>
                """, unsafe_allow_html=True)

            # Itemized Violation Logs Table
            st.markdown(f"###### ⚠️ Itemized Violation Logs ({len(violations)} Detected):")
            if violations:
                for v in violations:
                    sev = v.get("severity", "Minor")
                    sev_class = f"severity-{sev.lower()}"
                    st.markdown(f"""
                        <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <b style="color: #FFFFFF; font-size: 0.95rem;">{v.get('hazard_title', 'Hazard')}</b>
                                <span class="{sev_class}">{sev.upper()}</span>
                            </div>
                            <div style="font-size: 0.83rem; color: #D1D5DB; margin-bottom: 4px;">
                                <b>Visual Observation:</b> {v.get('observation', '')}
                            </div>
                            <div style="font-size: 0.8rem; color: #9CA3AF; margin-bottom: 4px;">
                                <b>Standard / Code:</b> <span style="color: #FBBF24;">{v.get('haccp_code', 'FDA Food Code')}</span>
                            </div>
                            <div style="font-size: 0.83rem; color: #34D399;">
                                <b>Immediate Corrective Action:</b> {v.get('corrective_action', '')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 No active safety violations or cross-contamination hazards detected.")

            # Summary
            st.markdown(f"""
                <div class="glass-card" style="margin-top: 10px;">
                    <b style="color: #10B981;">📋 Lead Inspector Summary:</b>
                    <p style="color: #D1D5DB; font-size: 0.88rem; margin: 4px 0 0 0;">{summary}</p>
                </div>
            """, unsafe_allow_html=True)

            # Download Audit
            st.download_button(
                "📥 Export Full HACCP Audit (JSON)",
                data=json.dumps(res, indent=2),
                file_name=f"haccp_audit_{scene_name.lower().replace(' ', '_')}.json",
                mime="application/json",
                key="dl_hygiene_json"
            )
        else:
            st.info("👈 Select a kitchen scenario or upload a photo to launch visual hygiene compliance inspection.")
