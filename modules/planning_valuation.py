"""
Tab 3: Planning & Real Estate Valuation Module (Epic 3).
Interactive inputs for structure type, built-up sqft, location tier (Tier 1/2/3 Indian cities),
and completion percentage slider. Calculates total project budget, CapEx incurred,
current market asset valuation in INR (Lakhs/Crores), steel/cement requirement metrics,
milestone progress bar, and conceptual 3D architectural rendering via Pollinations AI.
"""

import random
import urllib.parse
import streamlit as st

from utils.helpers import format_inr, format_inr_indian_commas
from utils.charts import create_budget_capex_chart, create_materials_progress_chart

# Benchmark Cost & Pricing Data (CPWD & Indian Real Estate Industry Benchmarks 2025-2026)
BENCHMARK_RATES = {
    "Residential High-Rise (G+20)": {
        "base_cost_sqft": 2600,
        "steel_kg_sqft": 4.2,      # 4.2 kg steel per sqft
        "cement_bags_sqft": 0.42,   # 0.42 bags (50kg) per sqft
        "selling_price_tier1": 12500,
        "selling_price_tier2": 7200,
        "selling_price_tier3": 4500,
        "prompt_style": "photorealistic modern luxury residential high-rise glass skyscraper architectural 3D render, golden hour sunlight, landscaped podium, parametric balconies"
    },
    "Commercial Complex / Tech Park": {
        "base_cost_sqft": 3200,
        "steel_kg_sqft": 5.2,
        "cement_bags_sqft": 0.46,
        "selling_price_tier1": 16500,
        "selling_price_tier2": 9500,
        "selling_price_tier3": 5800,
        "prompt_style": "ultra-modern Grade-A commercial corporate tech park building, double glazed curtain facade, dynamic architectural lighting, LEED platinum sustainable architecture"
    },
    "Industrial PEB Warehouse / Logistics Park": {
        "base_cost_sqft": 1850,
        "steel_kg_sqft": 6.0,
        "cement_bags_sqft": 0.32,
        "selling_price_tier1": 5500,
        "selling_price_tier2": 3800,
        "selling_price_tier3": 2600,
        "prompt_style": "state-of-the-art logistics warehouse pre-engineered building, heavy structural steel trusses, loading docks, solar panel roof, clean architectural photography"
    },
    "Luxury Villa Community": {
        "base_cost_sqft": 3600,
        "steel_kg_sqft": 3.8,
        "cement_bags_sqft": 0.45,
        "selling_price_tier1": 21000,
        "selling_price_tier2": 11500,
        "selling_price_tier3": 6800,
        "prompt_style": "contemporary tropical luxury villa estate, infinity swimming pool, travertine marble accents, floor-to-ceiling glass, lush landscaping, architectural drone render"
    },
    "Institutional / Healthcare Hospital": {
        "base_cost_sqft": 3900,
        "steel_kg_sqft": 5.0,
        "cement_bags_sqft": 0.48,
        "selling_price_tier1": 15000,
        "selling_price_tier2": 8800,
        "selling_price_tier3": 5400,
        "prompt_style": "modern tertiary multi-specialty hospital medical center, clean aesthetic facade, helipad, healing gardens, ambulance triage bay, realistic 3D render"
    }
}

TIER_MULTIPLIERS = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Hyderabad)": {"cost_factor": 1.22, "key": "selling_price_tier1", "tier_name": "Tier 1 Metro"},
    "Tier 2 (Pune, Ahmedabad, Jaipur, Kolkata, Surat)": {"cost_factor": 1.05, "key": "selling_price_tier2", "tier_name": "Tier 2 Urban"},
    "Tier 3 (Growing Hubs, Coimbatore, Indore, Nagpur)": {"cost_factor": 0.92, "key": "selling_price_tier3", "tier_name": "Tier 3 Regional"}
}

SPEC_GRADE_MULTIPLIER = {
    "Standard / Economy Grade": 0.90,
    "Executive / Premium Grade": 1.00,
    "Ultra-Luxury / High-Spec Grade": 1.25
}

def render_planning_valuation_tab():
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #F8FAFC; margin-bottom: 4px; font-weight: 700;">
                🏗️ Planning, Material Estimation & Real Estate Valuation
            </h2>
            <div style="color: #94A3B8; font-size: 0.95rem;">
                Civil Engineering CapEx Modeling, Quantity Surveying (Steel/Cement Thumb Rules),
                Indian Real Estate Asset Valuation (₹ Lakhs & ₹ Crores), and AI Conceptual 3D Architectural Visualization.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_finance = st.columns([1, 1], gap="large")

    with col_ctrl:
        st.markdown("### ⚙️ 1. Project Parameters & Physical Scale")
        
        structure_type = st.selectbox(
            "Structure Typology:",
            list(BENCHMARK_RATES.keys()),
            index=0
        )

        location_tier = st.selectbox(
            "Location Tier (Indian Market):",
            list(TIER_MULTIPLIERS.keys()),
            index=0
        )

        grade = st.selectbox(
            "Specification & Finishes Grade:",
            list(SPEC_GRADE_MULTIPLIER.keys()),
            index=1
        )

        built_up_sqft = st.number_input(
            "Total Built-Up Area (sq. ft.):",
            min_value=1000,
            max_value=2000000,
            value=85000,
            step=5000,
            help="Total gross construction floor area across all levels."
        )

        st.markdown("#### ⏳ Project Construction Progress")
        completion_pct = st.slider(
            "Current Milestone Completion (%):",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            format="%d%%"
        )

        # Milestone Stage Resolver
        if completion_pct < 15:
            milestone_stage = "Substructure: Excavation, Piling & Raft Foundation"
            milestone_badge = "badge-slate"
        elif completion_pct < 45:
            milestone_stage = "Superstructure: RCC Columns, Beams & Slab Casting"
            milestone_badge = "badge-amber"
        elif completion_pct < 75:
            milestone_stage = "Mid-Stage: AAC Block Masonry, MEP Conduiting & Plastering"
            milestone_badge = "badge-cyan"
        elif completion_pct < 95:
            milestone_stage = "Finishing: Flooring, Glazing Facade, Lift Installation"
            milestone_badge = "badge-purple"
        else:
            milestone_stage = "Commissioning: Testing, Snag Rectification & Occupancy Handover"
            milestone_badge = "badge-emerald"

        st.markdown(f"""
            <div style="margin-top: 6px;">
                <span class="pill-badge {milestone_badge}">📍 Milestone: {milestone_stage}</span>
            </div>
        """, unsafe_allow_html=True)

    # Core Calculations
    struct_info = BENCHMARK_RATES[structure_type]
    tier_info = TIER_MULTIPLIERS[location_tier]
    grade_factor = SPEC_GRADE_MULTIPLIER[grade]

    # Adjusted construction cost per sqft
    unit_cost_sqft = struct_info["base_cost_sqft"] * tier_info["cost_factor"] * grade_factor
    total_budget_inr = built_up_sqft * unit_cost_sqft
    capex_incurred_inr = total_budget_inr * (completion_pct / 100.0)
    cost_to_complete_inr = total_budget_inr - capex_incurred_inr

    # Market Valuation: Built-up * selling price per sqft, discounted for stage
    market_selling_rate = struct_info[tier_info["key"]] * grade_factor
    full_completed_asset_val_inr = built_up_sqft * market_selling_rate
    # Stage valuation = CapEx incurred + land & developer equity value share (e.g. 50% baseline + completion % * 50%)
    current_asset_valuation_inr = full_completed_asset_val_inr * (0.35 + 0.65 * (completion_pct / 100.0))

    # Materials Thumb Rules
    total_steel_kg = built_up_sqft * struct_info["steel_kg_sqft"]
    total_steel_mt = total_steel_kg / 1000.0  # Metric Tonnes
    steel_used_mt = total_steel_mt * (completion_pct / 100.0)

    total_cement_bags = built_up_sqft * struct_info["cement_bags_sqft"]
    cement_used_bags = total_cement_bags * (completion_pct / 100.0)
    total_cement_tonnes = total_cement_bags * 0.05
    cement_used_tonnes = cement_used_bags * 0.05

    budget_cr = total_budget_inr / 10_000_000.0
    capex_cr = capex_incurred_inr / 10_000_000.0
    valuation_cr = current_asset_valuation_inr / 10_000_000.0

    with col_finance:
        st.markdown("### 💰 2. Financial Metrics & Real Estate Valuation")

        # Metric Cards Grid
        f1, f2 = st.columns(2)
        with f1:
            st.markdown(f"""
                <div class="metric-card cyan">
                    <div class="metric-label">Total Project Budget</div>
                    <div class="metric-value">{format_inr(total_budget_inr)}</div>
                    <div class="metric-sub">{format_inr_indian_commas(total_budget_inr)} &bull; ₹{unit_cost_sqft:,.0f}/sqft</div>
                </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown(f"""
                <div class="metric-card amber">
                    <div class="metric-label">CapEx Incurred to Date</div>
                    <div class="metric-value">{format_inr(capex_incurred_inr)}</div>
                    <div class="metric-sub">{completion_pct}% of budget realized</div>
                </div>
            """, unsafe_allow_html=True)

        f3, f4 = st.columns(2)
        with f3:
            st.markdown(f"""
                <div class="metric-card emerald">
                    <div class="metric-label">Current Market Valuation</div>
                    <div class="metric-value">{format_inr(current_asset_valuation_inr)}</div>
                    <div class="metric-sub">At {completion_pct}% completion stage</div>
                </div>
            """, unsafe_allow_html=True)
        with f4:
            st.markdown(f"""
                <div class="metric-card purple">
                    <div class="metric-label">Projected Final Asset Value</div>
                    <div class="metric-value">{format_inr(full_completed_asset_val_inr)}</div>
                    <div class="metric-sub">₹{market_selling_rate:,.0f}/sqft market benchmark</div>
                </div>
            """, unsafe_allow_html=True)

        # Plotly CapEx Waterfall / Progress
        st.plotly_chart(create_budget_capex_chart(budget_cr, capex_cr, completion_pct), use_container_width=True)

    st.markdown("---")

    # Lower Grid: Material Surveying & 3D Architectural Rendering
    col_mat, col_render = st.columns([1, 1], gap="large")

    with col_mat:
        st.markdown("### 🧱 3. Quantity Surveying: Steel & Cement Requirement")
        st.markdown("""
            Quantity estimation calculated utilizing standard **CPWD (Central Public Works Department)** 
            and **IS 10262** structural engineering consumption constants:
        """)

        sm1, sm2 = st.columns(2)
        with sm1:
            st.markdown(f"""
                <div class="glass-card">
                    <span style="color: #06B6D4; font-weight: 700; font-size: 0.82rem; text-transform: uppercase;">Structural TMT Steel</span>
                    <h3 style="margin: 4px 0; color: #FFFFFF; font-family: 'JetBrains Mono'; font-size: 1.5rem;">
                        {total_steel_mt:,.1f} <span style="font-size: 0.9rem; color: #94A3B8;">MT</span>
                    </h3>
                    <div style="color: #94A3B8; font-size: 0.8rem;">
                        <b>Incurred:</b> {steel_used_mt:,.1f} MT &bull; <b>Remaining:</b> {max(0, total_steel_mt - steel_used_mt):,.1f} MT<br/>
                        <b>Thumb rule:</b> {struct_info['steel_kg_sqft']} kg / sq. ft.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with sm2:
            st.markdown(f"""
                <div class="glass-card">
                    <span style="color: #F59E0B; font-weight: 700; font-size: 0.82rem; text-transform: uppercase;">OPC / PPC Cement</span>
                    <h3 style="margin: 4px 0; color: #FFFFFF; font-family: 'JetBrains Mono'; font-size: 1.5rem;">
                        {total_cement_bags:,.0f} <span style="font-size: 0.9rem; color: #94A3B8;">Bags</span>
                    </h3>
                    <div style="color: #94A3B8; font-size: 0.8rem;">
                        <b>Total Weight:</b> {total_cement_tonnes:,.1f} Tonnes<br/>
                        <b>Poured to date:</b> {cement_used_bags:,.0f} bags ({cement_used_tonnes:,.1f} T)<br/>
                        <b>Thumb rule:</b> {struct_info['cement_bags_sqft']} bags / sq. ft.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Plotly Materials Stacked Bar
        st.plotly_chart(
            create_materials_progress_chart(total_steel_mt, steel_used_mt, total_cement_tonnes, cement_used_tonnes),
            use_container_width=True
        )

    with col_render:
        st.markdown("### 🎨 4. Conceptual 3D Architectural Rendering")
        st.markdown("""
            Automated architectural prompt generation and neural synthesis integrated via **Pollinations AI**:
        """)

        # Generate contextual prompt based on inputs
        tier_short = tier_info["tier_name"]
        style_desc = struct_info["prompt_style"]
        
        dynamic_prompt = (
            f"{style_desc}, {structure_type} located in {tier_short} India, {grade}, "
            f"exterior architectural perspective, volumetric lighting, photorealistic 8k octane render"
        )

        # Allow user to seed or modify
        if "render_seed" not in st.session_state:
            st.session_state["render_seed"] = random.randint(1000, 999999)

        c_prompt, c_regen = st.columns([3, 1])
        with c_prompt:
            custom_prompt = st.text_area(
                "Dynamic Neural Architectural Prompt:",
                value=dynamic_prompt,
                height=70
            )
        with c_regen:
            st.write("")
            st.write("")
            if st.button("🎲 New Seed", use_container_width=True):
                st.session_state["render_seed"] = random.randint(1000, 999999)

        # Encode URL for Pollinations AI
        encoded_prompt = urllib.parse.quote(custom_prompt.strip())
        current_seed = st.session_state["render_seed"]
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&seed={current_seed}&nologo=true"

        # Display Rendering
        st.image(
            pollinations_url,
            caption=f"Conceptual 3D BIM Render: {structure_type} (Seed: {current_seed})",
            use_container_width=True
        )

        st.markdown(f"""
            <div style="text-align: right; margin-top: 4px;">
                <a href="{pollinations_url}" target="_blank" style="color: #F59E0B; font-size: 0.85rem; text-decoration: none;">
                    🔗 Open High-Res Rendering in New Tab &rarr;
                </a>
            </div>
        """, unsafe_allow_html=True)
