"""
Tab 2: Crack Diagnostics & Structural Integrity Module (Epic 2).
Multimodal classification of defects (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling)
with estimated width (mm), root causes, engineering repairs, and urgency under IS 456 & ACI codes.
"""

import json
from datetime import datetime
from PIL import Image
import streamlit as st

from modules.ai_service import ConstructionAIService
from modules.demo_data import DEMO_CRACKS
from utils.charts import create_crack_width_gauge

def render_crack_diagnostics_tab(ai_service: ConstructionAIService):
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #F8FAFC; margin-bottom: 4px; font-weight: 700;">
                🔬 Crack Diagnostics & Structural Integrity Assessment
            </h2>
            <div style="color: #94A3B8; font-size: 0.95rem;">
                Forensic structural computer vision grounded in <b>IS 456:2000 (Clause 35.3.2)</b>, <b>IS 13920:2016</b>, and <b>ACI 224R</b>.
                Classifies defect pathology, estimates crack aperture in mm, flags structural shear risks, and specifies chemical repair protocols.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 📷 1. Concrete / Wall Defect Inspection")
        photo_choice = st.radio(
            "Select Concrete Surface Source:",
            ["Preset Structural Pathology Images", "Upload Concrete / Masonry Image"],
            index=0,
            horizontal=True
        )

        selected_image = None
        element_context = ""

        if photo_choice == "Preset Structural Pathology Images":
            preset_crack_name = st.selectbox(
                "Choose Structural Pathology Scenario:",
                list(DEMO_CRACKS.keys()),
                index=0
            )
            preset_data = DEMO_CRACKS[preset_crack_name]
            element_context = f"{preset_crack_name} ({preset_data['element']})"
            st.image(preset_data["image_url"], caption=f"Defect: {preset_crack_name}", use_container_width=True)
            selected_image = preset_data["image_url"]
        else:
            uploaded_crack = st.file_uploader(
                "Upload High-Resolution Concrete Surface Photo:",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear close-up of the cracked beam, column, slab, or foundation masonry."
            )
            element_context = st.text_input(
                "Element & Location Context:",
                placeholder="e.g. Column C-4 Joint, Shear Wall Level 2, Cantilever Balcony Beam"
            )
            if uploaded_crack:
                selected_image = Image.open(uploaded_crack)
                st.image(selected_image, caption="Uploaded Surface Inspection Photo", use_container_width=True)

        st.markdown("---")
        run_diag_btn = st.button(
            "⚡ Diagnose Crack & Structural Integrity",
            type="primary",
            use_container_width=True
        )

    # Maintain state
    if "crack_diagnostic_data" not in st.session_state:
        st.session_state["crack_diagnostic_data"] = DEMO_CRACKS["Structural Shear Crack at Beam-Column Joint"]

    if run_diag_btn:
        if not selected_image:
            st.error("⚠️ Please select a preset defect image or upload a concrete surface photo.")
        else:
            with st.spinner("Analyzing concrete surface pathology, stress patterns & aperture..."):
                diag_result = ai_service.diagnose_crack_structural(
                    image_input=selected_image,
                    element_context=element_context
                )
                st.session_state["crack_diagnostic_data"] = diag_result
                st.success("✅ Structural Diagnostic Complete!")

    # Display Diagnostic Card
    res = st.session_state.get("crack_diagnostic_data", {})
    if res:
        defect_type = res.get("defect_type", "Structural Crack")
        width_mm = float(res.get("estimated_width_mm", 0.5))
        limit_mm = float(res.get("is456_exposure_limit_mm", 0.20))
        urgency = res.get("urgency", "Moderate")
        element = res.get("element", "RCC Element")
        root_causes = res.get("root_causes", "Stress distribution exceedance.")
        repairs = res.get("engineering_repairs", [])
        standards = res.get("standards_reference", "IS 456:2000, ACI 224R")

        with col_output:
            st.markdown("### 📐 2. Structural Defect Analysis")

            # Urgency pill and classification
            urgency_lower = urgency.lower()
            if "urgent" in urgency_lower or "crit" in urgency_lower or "evac" in urgency_lower:
                urgency_badge = '<span class="pill-badge badge-rose">🚨 ' + urgency + '</span>'
            elif "mod" in urgency_lower:
                urgency_badge = '<span class="pill-badge badge-amber">⚠️ ' + urgency + '</span>'
            else:
                urgency_badge = '<span class="pill-badge badge-emerald">✓ ' + urgency + '</span>'

            st.markdown(f"""
                <div class="glass-card-accent">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                        <div>
                            <span style="color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;">Defect Classification</span>
                            <h3 style="color: #F8FAFC; margin: 2px 0 0 0; font-size: 1.35rem;">{defect_type}</h3>
                        </div>
                        {urgency_badge}
                    </div>
                    <div style="color: #64748B; font-size: 0.85rem; margin-top: 4px;">
                        📍 <b>Structural Element:</b> {element}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Metrics
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"""
                    <div class="metric-card {'rose' if width_mm > limit_mm else 'emerald'}">
                        <div class="metric-label">Estimated Width</div>
                        <div class="metric-value">{width_mm:.2f} <span style="font-size: 1rem; color: #64748B;">mm</span></div>
                        <div class="metric-sub">IS 456 Limit: {limit_mm:.2f} mm</div>
                    </div>
                """, unsafe_allow_html=True)
            with m2:
                exceeds = width_mm > limit_mm
                st.markdown(f"""
                    <div class="metric-card {'rose' if exceeds else 'emerald'}">
                        <div class="metric-label">Threshold Status</div>
                        <div class="metric-value" style="font-size: 1.3rem;">{ 'EXCEEDS LIMIT' if exceeds else 'WITHIN LIMIT' }</div>
                        <div class="metric-sub">{f"+{(width_mm - limit_mm):.2f} mm delta" if exceeds else "Safe for exposure"}</div>
                    </div>
                """, unsafe_allow_html=True)

            # Plotly Gauge for Crack Width vs Code Limit
            st.plotly_chart(create_crack_width_gauge(width_mm, limit_mm), use_container_width=True)

        st.markdown("---")

        # Deep Engineering Root Cause & Repair Breakdown
        st.markdown("### 🛠️ 3. Forensic Mechanics & Engineering Repair Protocols")
        
        c_cause, c_repair = st.columns([1, 1], gap="medium")
        with c_cause:
            st.markdown("""
                <div class="glass-card" style="height: 100%;">
                    <h4 style="color: #F59E0B; margin: 0 0 8px 0;">🔬 Root Cause & Failure Mechanism</h4>
            """, unsafe_allow_html=True)
            st.write(root_causes)
            st.markdown(f"""
                    <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.06); color: #94A3B8; font-size: 0.82rem;">
                        <b>Design Code Benchmark:</b> <code>{standards}</code><br/>
                        <b>Remediation Timeframe:</b> <span style="color: #FBBF24;">{res.get('remediation_urgency_days', 'Within 7 Days')}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with c_repair:
            st.markdown("""
                <div class="glass-card" style="height: 100%;">
                    <h4 style="color: #06B6D4; margin: 0 0 8px 0;">📋 Step-by-Step Engineering Repair Specification</h4>
            """, unsafe_allow_html=True)
            for idx, step in enumerate(repairs, start=1):
                st.markdown(f"""
                    <div style="margin-bottom: 10px; padding: 10px; background: rgba(15, 23, 42, 0.7); border-radius: 8px; border-left: 3px solid #06B6D4;">
                        <span style="font-weight: 700; color: #67E8F9; font-size: 0.85rem;">Step {idx}:</span>
                        <div style="color: #E2E8F0; font-size: 0.88rem; margin-top: 2px; line-height: 1.5;">{step}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        
        # Download Diagnostic Report
        st.markdown("#### 💾 Export Diagnostic Report")
        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            st.download_button(
                label="📥 Download Structured Diagnostic JSON",
                data=json.dumps(res, indent=2),
                file_name=f"crack_structural_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_d2:
            report_text = f"""# STRUCTURAL CRACK PATHOLOGY & INTEGRITY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Defect Classification: {defect_type}
Element: {element}
Estimated Width: {width_mm:.2f} mm
IS 456 Permissible Limit: {limit_mm:.2f} mm
Urgency: {urgency}
Standards: {standards}

ROOT CAUSE ANALYSIS:
{root_causes}

RECOMMENDED ENGINEERING REPAIR SPECIFICATION:
""" + "\n".join([f"{i}. {s}" for i, s in enumerate(repairs, 1)])
            st.download_button(
                label="📄 Download Diagnostic Summary (.txt)",
                data=report_text,
                file_name=f"crack_diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
