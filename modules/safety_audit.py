"""
Tab 1: Site Safety & PPE Audit Module (Epic 2).
Multimodal worker PPE compliance (Helmets, High-Vis, Steel-Toe Boots, Safety Harnesses)
under OSHA 1926 and IS 456 / IS 3696 standards with structured reporting and metrics.
"""

import json
from datetime import datetime
from PIL import Image
import streamlit as st

from modules.ai_service import ConstructionAIService
from modules.demo_data import DEMO_PPE_SITES
from utils.helpers import (
    get_safety_score_badge,
    get_severity_badge_class,
    generate_audit_markdown_report
)
from utils.charts import create_safety_gauge, create_hazard_breakdown_donut

def render_safety_audit_tab(ai_service: ConstructionAIService):
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #F8FAFC; margin-bottom: 4px; font-weight: 700;">
                🦺 Site Safety & Worker PPE Compliance Audit
            </h2>
            <div style="color: #94A3B8; font-size: 0.95rem;">
                Autonomous Computer Vision Inspection grounded in <b>OSHA 1926 Subpart E & M</b> and Indian <b>IS 456 / IS 3696</b> standards.
                Detects helmets, high-vis vests, steel-toe boots, fall arrest harnesses, and physical site hazards.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_view = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("### 📸 1. Site Photo Input")
        input_source = st.radio(
            "Select Photo Source:",
            ["Preset High-Resolution Test Images", "Upload Construction Site Photo (JPG/PNG)"],
            index=0,
            horizontal=True
        )

        selected_image = None
        site_context = ""

        if input_source == "Preset High-Resolution Test Images":
            preset_choice = st.selectbox(
                "Choose Active Construction Site Scenario:",
                list(DEMO_PPE_SITES.keys()),
                index=0
            )
            preset_meta = DEMO_PPE_SITES[preset_choice]
            site_context = f"{preset_choice} - {preset_meta['zone']}"
            
            # Display preset preview
            st.image(preset_meta["image_url"], caption=f"Scenario: {preset_choice} ({preset_meta['zone']})", use_container_width=True)
            selected_image = preset_meta["image_url"]
        else:
            uploaded_file = st.file_uploader(
                "Upload Site Photo (JPG / PNG):",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear photograph of construction workers, scaffolding, excavation, or slab deck."
            )
            site_context = st.text_input(
                "Optional Site / Zone Location Hint:",
                placeholder="e.g. Tower A Floor 18 Slab Casting, Basement Sump, Facade Scaffold"
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)
                st.image(selected_image, caption="Uploaded Construction Site Photograph", use_container_width=True)

        st.markdown("---")
        run_audit_btn = st.button(
            "🔍 Run Multimodal Safety & PPE Audit",
            type="primary",
            use_container_width=True
        )

    # Maintain analysis result in session state
    if "safety_audit_data" not in st.session_state:
        # Pre-seed with default demo scenario for instantaneous showcase
        st.session_state["safety_audit_data"] = DEMO_PPE_SITES["Active High-Rise Slab Rebar & Concreting"]

    if run_audit_btn:
        if not selected_image:
            st.error("⚠️ Please select a preset scenario or upload a construction site photo.")
        else:
            with st.spinner("Analyzing worker PPE and site hazards via Multimodal Vision Engine..."):
                result = ai_service.audit_site_safety_ppe(
                    image_input=selected_image,
                    site_context=site_context
                )
                st.session_state["safety_audit_data"] = result
                st.success("✅ Multimodal Safety Audit Complete!")

    # Display Results
    data = st.session_state.get("safety_audit_data", {})
    if data:
        score = data.get("safety_score", 0)
        status = data.get("overall_status", "Needs Attention")
        workers = data.get("workers_detected", 0)
        hazards = data.get("site_hazards", [])
        ppe_items = data.get("ppe_detection", [])
        badge_label, badge_class, _ = get_safety_score_badge(score)

        with col_view:
            st.markdown("### 📊 2. Regulatory Compliance Overview")
            
            # Metric Card Grid
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                    <div class="metric-card {'emerald' if score>=85 else 'amber' if score>=65 else 'rose'}">
                        <div class="metric-label">Safety Score</div>
                        <div class="metric-value">{score} <span style="font-size: 1rem; color: #64748B;">/100</span></div>
                        <div class="metric-sub">{status}</div>
                    </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                    <div class="metric-card cyan">
                        <div class="metric-label">Workers Detected</div>
                        <div class="metric-value">{workers}</div>
                        <div class="metric-sub">Active in Frame</div>
                    </div>
                """, unsafe_allow_html=True)
            with m3:
                critical_count = sum(1 for h in hazards if "crit" in h.get("severity", "").lower())
                st.markdown(f"""
                    <div class="metric-card {'rose' if critical_count > 0 else 'emerald'}">
                        <div class="metric-label">Critical Hazards</div>
                        <div class="metric-value">{critical_count}</div>
                        <div class="metric-sub">Stop-Work Level</div>
                    </div>
                """, unsafe_allow_html=True)

            # Visual Indicator Gauges
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.plotly_chart(create_safety_gauge(score), use_container_width=True)
            with g_col2:
                st.plotly_chart(create_hazard_breakdown_donut(hazards), use_container_width=True)

        st.markdown("---")

        # Full Width Detailed Inspection Breakdowns
        tab_ppe, tab_hazards, tab_json = st.tabs([
            "📋 PPE Compliance Checklist",
            "⚠️ Identified Site Hazards & Remediation",
            "💾 Structured JSON & Export"
        ])

        with tab_ppe:
            st.markdown("#### 🦺 Worker Personal Protective Equipment (PPE) Matrix")
            st.markdown(f"""
                <div style="margin-bottom: 12px;">
                    <span class="pill-badge {badge_class}">{badge_label}</span>
                    <span class="pill-badge badge-slate">Standard: OSHA 29 CFR 1926 & IS 456</span>
                </div>
            """, unsafe_allow_html=True)

            # Build HTML table for PPE
            table_html = """
            <table class="ppe-table">
                <thead>
                    <tr>
                        <th>Equipment Item</th>
                        <th>Detection Status</th>
                        <th>Compliance Ratio</th>
                        <th>Standard Reference</th>
                        <th>Inspector Observations & Code Directives</th>
                    </tr>
                </thead>
                <tbody>
            """
            for item in ppe_items:
                st_val = item.get("status", "N/A")
                if st_val.lower() == "detected":
                    status_pill = '<span class="pill-badge badge-emerald">✓ Detected</span>'
                elif st_val.lower() == "partial":
                    status_pill = '<span class="pill-badge badge-amber">⚠ Partial</span>'
                elif "non" in st_val.lower() or "missing" in st_val.lower():
                    status_pill = '<span class="pill-badge badge-rose">✕ Missing</span>'
                else:
                    status_pill = '<span class="pill-badge badge-slate">N/A</span>'

                table_html += f"""
                    <tr>
                        <td><b>{item.get('item', 'Item')}</b></td>
                        <td>{status_pill}</td>
                        <td><span style="font-family: 'JetBrains Mono'; font-weight: 600;">{item.get('compliance_rate', 'N/A')}</span></td>
                        <td><code>{item.get('code_reference', 'OSHA 1926')}</code></td>
                        <td>{item.get('notes', '')}</td>
                    </tr>
                """
            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)

        with tab_hazards:
            st.markdown("#### 🚨 Physical Site Hazards & Corrective Engineering Action Plans")
            if not hazards:
                st.success("🎉 No high-severity site hazards detected in this inspection frame.")
            else:
                for idx, h in enumerate(hazards, start=1):
                    sev = h.get("severity", "Medium")
                    sev_class = get_severity_badge_class(sev)
                    
                    st.markdown(f"""
                        <div class="glass-card" style="border-left: 4px solid {'#EF4444' if 'crit' in sev.lower() else '#F97316' if 'high' in sev.lower() else '#EAB308'};">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC;">
                                    #{idx}. {h.get('hazard_type', 'Unclassified')}
                                </span>
                                <span class="{sev_class}">{sev.upper()} SEVERITY</span>
                            </div>
                            <div style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 8px;">
                                📍 <b>Location:</b> {h.get('location', 'Site Perimeter')} &bull; 
                                📜 <b>Regulatory Reference:</b> <code>{h.get('regulatory_code', 'OSHA 1926')}</code>
                            </div>
                            <div style="background: rgba(15, 23, 42, 0.7); border-radius: 8px; padding: 12px; margin-top: 6px;">
                                <div style="color: #FBBF24; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Corrective Action & Engineering Remedy:</div>
                                <div style="color: #E2E8F0; font-size: 0.88rem; margin-top: 4px; line-height: 1.5;">
                                    {h.get('corrective_remedy', 'Immediate remediation advised.')}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if "executive_summary" in data:
                st.markdown(f"""
                    <div class="glass-card" style="margin-top: 14px;">
                        <h4 style="margin: 0 0 6px 0; color: #F59E0B;">📋 Executive Safety Assessment</h4>
                        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                            {data['executive_summary']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

        with tab_json:
            st.markdown("#### 💾 Structured JSON Audit Record")
            st.json(data)
            
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.download_button(
                    label="📥 Download JSON Audit Report",
                    data=json.dumps(data, indent=2),
                    file_name=f"construction_safety_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with d_col2:
                markdown_doc = generate_audit_markdown_report(data, project_name=site_context or "Active Site")
                st.download_button(
                    label="📄 Download Formatted Inspection Document (.md)",
                    data=markdown_doc,
                    file_name=f"site_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
