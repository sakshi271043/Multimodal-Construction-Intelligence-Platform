"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
Production-ready Streamlit application in Python.
Zero external database dependencies. 1-click deploy ready for Streamlit Community Cloud.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load optional local .env file
load_dotenv()

from utils.styles import inject_custom_styles
from modules.ai_service import ConstructionAIService
from modules.safety_audit import render_safety_audit_tab
from modules.crack_diagnostics import render_crack_diagnostics_tab
from modules.planning_valuation import render_planning_valuation_tab
from modules.site_assistant import render_site_assistant_tab

# Streamlit Page Setup
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Industrial Glassmorphism Styling
inject_custom_styles()

def main():
    # Sidebar Configuration & Architecture Overview
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding-bottom: 12px;">
                <span style="font-size: 2.8rem;">🏗️</span>
                <h2 style="color: #F59E0B; margin: 4px 0 0 0; font-weight: 800; letter-spacing: -0.5px;">Construction AI</h2>
                <span style="color: #94A3B8; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                    Skill Wallet Capstone Project 1
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⚙️ Intelligence Engine & API")

        # Provider Mode Selection
        provider_mode = st.radio(
            "Select Intelligence Mode:",
            ["Standalone Demonstration Mode", "Google Gemini Live Multimodal"],
            index=0,
            key="cfg_provider_mode",
            help="Demonstration mode runs 100% offline with zero API key required."
        )

        api_key = ""
        model_name = "gemini-2.5-flash"
        active_provider = "demo"

        if provider_mode == "Google Gemini Live Multimodal":
            active_provider = "gemini"
            env_key = os.getenv("GEMINI_API_KEY", "")
            
            # Also check Streamlit secrets if running in cloud
            if not env_key and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                env_key = st.secrets["GEMINI_API_KEY"]

            api_key = st.text_input(
                "Gemini API Key:",
                value=env_key,
                type="password",
                help="Enter your Google Gemini API key. If left blank, automatically falls back to demonstration mode.",
                placeholder="AIzaSy..."
            )
            model_name = st.selectbox(
                "Gemini Model Architecture:",
                ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
                index=0
            )
            if not api_key:
                st.warning("⚠️ No Gemini key supplied. Automatically activating Demonstration Mode fallback.")
                active_provider = "demo"
        else:
            active_provider = "demo"
            st.success("🟢 Demonstration Mode Active (Instant Zero-Key Evaluation).")

        # Provider Status Badge
        st.markdown("---")
        if active_provider == "demo":
            st.markdown("""
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 10px; text-align: center;">
                    <span style="color: #FBBF24; font-weight: 700; font-size: 0.85rem;">🟡 Mode: Demonstration Showcase</span><br/>
                    <span style="color: #94A3B8; font-size: 0.75rem;">Instant Multi-Scenario Intelligence</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px; text-align: center;">
                    <span style="color: #34D399; font-weight: 700; font-size: 0.85rem;">🟢 Live Gemini Multimodal Connected</span><br/>
                    <span style="color: #94A3B8; font-size: 0.75rem;">Model: {model_name}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🏛️ Architecture & Knowledge Hub")
        st.markdown("""
            <div style="color: #94A3B8; font-size: 0.82rem; line-height: 1.6;">
                • <b>Multimodal Vision 2.5:</b> Visual PPE & Crack Sensor<br/>
                • <b>OSHA 1926:</b> Worker Personal Protection Safety<br/>
                • <b>IS 456:2000:</b> Plain & Reinforced Concrete Limits<br/>
                • <b>IS 13920 & ACI 224:</b> Ductile Detailing & Crack Repair<br/>
                • <b>IS 875 (Part 3):</b> High Wind & Cyclone Protocols<br/>
                • <b>CPWD Benchmarks:</b> Steel & Cement Quantity Surveying<br/>
                • <b>Pollinations AI:</b> Generative 3D BIM Concepts
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Reset / Clear Session Cache", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        st.markdown("""
            <div style="margin-top: 20px; text-align: center; color: #64748B; font-size: 0.75rem;">
                Multimodal Construction Intelligence &bull; Capstone 1<br/>
                Zero External DB &bull; 100% Streamlit Cloud Native
            </div>
        """, unsafe_allow_html=True)

    # Initialize AI Multi-Provider Service
    ai_service = ConstructionAIService(
        provider=active_provider,
        api_key=api_key,
        model_name=model_name
    )

    # Main Top Hero Banner
    st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">Multimodal Construction Intelligence Platform</h1>
            <div class="hero-subtitle">
                Skill Wallet Capstone Project 1: Next-generation multimodal AI architecture for autonomous site safety audits (OSHA/IS 456), 
                structural crack defect pathology & forensic repair specifications, real estate CapEx valuation in INR, and weather-aware engineering advisory.
            </div>
            <div class="badge-row">
                <span class="pill-badge badge-amber">⚡ Multimodal Vision 2.5</span>
                <span class="pill-badge badge-emerald">🦺 OSHA 1926 & IS 456 Grounded</span>
                <span class="pill-badge badge-rose">🔬 Forensic Crack Diagnostics</span>
                <span class="pill-badge badge-cyan">🏗️ Quantity Surveying (Steel & Cement)</span>
                <span class="pill-badge badge-purple">💰 Indian Real Estate Valuation (₹ Cr)</span>
                <span class="pill-badge badge-slate">🌦️ Dynamic Weather Field Advisories</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Core Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🦺 1. Site Safety & PPE Audit (Epic 2)",
        "🔬 2. Crack Diagnostics & Structural Integrity (Epic 2)",
        "🏗️ 3. Planning & Real Estate Valuation (Epic 3)",
        "🌦️ 4. Daily Site Assistant & Weather Advisory (Epic 5)"
    ])

    with tab1:
        render_safety_audit_tab(ai_service)

    with tab2:
        render_crack_diagnostics_tab(ai_service)

    with tab3:
        render_planning_valuation_tab()

    with tab4:
        render_site_assistant_tab(ai_service)

if __name__ == "__main__":
    main()
