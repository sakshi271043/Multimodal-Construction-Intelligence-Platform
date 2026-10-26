"""
Food Verse AI - Multimodal Food Intelligence Agent
Skill Wallet Capstone Project 3
Production-ready Streamlit application.
Zero external database dependencies. 1-click deploy ready for Streamlit Community Cloud.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load optional .env file
load_dotenv()

from utils.styles import inject_custom_styles
from modules.ai_service import FoodVerseAIService
from modules.nutrition_audit import render_nutrition_audit_tab
from modules.freshness_diagnostic import render_freshness_diagnostic_tab
from modules.hygiene_compliance import render_hygiene_compliance_tab
from modules.recipe_assistant import render_recipe_assistant_tab
from modules.meal_planner import render_meal_planner_tab

# Streamlit Page Setup
st.set_page_config(
    page_title="Food Verse AI - Multimodal Food Intelligence Agent",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Glassmorphism Styling
inject_custom_styles()

def main():
    # Sidebar Configuration & Persona Hub
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding-bottom: 12px;">
                <span style="font-size: 2.8rem;">🥗</span>
                <h2 style="color: #10B981; margin: 4px 0 0 0; font-weight: 800; letter-spacing: -0.5px;">Food Verse AI</h2>
                <span style="color: #9CA3AF; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                    Skill Wallet Capstone 3
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⚙️ Intelligence Engine & API")

        # Provider Selection
        provider_mode = st.radio(
            "Select Intelligence Provider:",
            ["Standalone Showcase / Demo Mode", "Google Gemini (Multimodal)", "Groq Cloud (Ultra-Fast)"],
            index=0,
            key="cfg_provider_mode"
        )

        api_key = ""
        model_name = ""
        active_provider = "demo"

        if provider_mode == "Google Gemini (Multimodal)":
            active_provider = "gemini"
            env_key = os.getenv("GEMINI_API_KEY", "")
            api_key = st.text_input(
                "Gemini API Key:",
                value=env_key,
                type="password",
                help="Enter your Google Gemini API key or set GEMINI_API_KEY environment variable.",
                placeholder="AIzaSy..."
            )
            model_name = st.selectbox(
                "Gemini Model:",
                ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
                index=0
            )
            if not api_key:
                st.warning("⚠️ No Gemini key provided. Automatically activating Standalone Showcase Fallback.")
                active_provider = "demo"
        elif provider_mode == "Groq Cloud (Ultra-Fast)":
            active_provider = "groq"
            env_key = os.getenv("GROQ_API_KEY", "")
            api_key = st.text_input(
                "Groq API Key:",
                value=env_key,
                type="password",
                help="Enter your Groq API key or set GROQ_API_KEY environment variable.",
                placeholder="gsk_..."
            )
            model_name = st.selectbox(
                "Groq Model:",
                ["llama-3.2-11b-vision-preview", "llama-3.3-70b-versatile"],
                index=0
            )
            if not api_key:
                st.warning("⚠️ No Groq key provided. Automatically activating Standalone Showcase Fallback.")
                active_provider = "demo"
        else:
            active_provider = "demo"
            st.success("🟢 Standalone Demonstration Mode Active (Zero API Key required).")

        # Provider Status Badge
        st.markdown("---")
        if active_provider == "demo":
            st.markdown("""
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 10px; text-align: center;">
                    <span style="color: #FBBF24; font-weight: 700; font-size: 0.85rem;">🟡 Mode: Standalone Showcase</span><br/>
                    <span style="color: #9CA3AF; font-size: 0.75rem;">Simulated Multimodal Intelligence</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px; text-align: center;">
                    <span style="color: #34D399; font-weight: 700; font-size: 0.85rem;">🟢 Live AI Connected: {active_provider.upper()}</span><br/>
                    <span style="color: #9CA3AF; font-size: 0.75rem;">Model: {model_name}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🧠 FoodVerse Persona")
        st.markdown("""
            <div style="color: #9CA3AF; font-size: 0.82rem; line-height: 1.5;">
                • <b>Executive Food Scientist</b><br/>
                • <b>HACCP Public Health Inspector</b><br/>
                • <b>Registered Clinical Dietitian</b><br/>
                • <b>Culinary Arts Master Chef</b>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Reset / Clear Session Cache", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        st.markdown("""
            <div style="margin-top: 24px; text-align: center; color: #6B7280; font-size: 0.75rem;">
                Food Verse AI &bull; Version 3.0<br/>
                Zero External DB &bull; 100% Cloud Native
            </div>
        """, unsafe_allow_html=True)

    # Initialize AI Service
    ai_service = FoodVerseAIService(
        provider=active_provider,
        api_key=api_key,
        model_name=model_name
    )

    # Main Hero Banner
    st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">Food Verse AI — Multimodal Food Intelligence Agent</h1>
            <div class="hero-subtitle">
                Skill Wallet Capstone Project 3: Next-generation culinary computer vision, clinical nutrition auditing, 
                perishable spoilage pathology, commercial kitchen HACCP compliance, and personalized metabolic meal planning.
            </div>
            <div class="badge-row">
                <span class="pill-badge badge-emerald">⚡ Multimodal Vision 2.5</span>
                <span class="pill-badge badge-cyan">🧬 Mifflin-St Jeor Bioenergetics</span>
                <span class="pill-badge badge-amber">🛡️ HACCP FDA Food Code Compliant</span>
                <span class="pill-badge badge-purple">♻️ Zero-Waste Culinary Hacks</span>
                <span class="pill-badge badge-rose">🧪 Pathogen & Spoilage Classifier</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Core Intelligence Navigation Pillars
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🥗 1. Nutrition Audit (Epic 2)",
        "🔬 2. Freshness Diagnostic (Epic 3)",
        "🧼 3. Kitchen Hygiene & Safety (Epic 4)",
        "🍳 4. Smart Recipe Assistant (Epic 4)",
        "📅 5. Personalized Meal Planner (Epic 5)"
    ])

    with tab1:
        render_nutrition_audit_tab(ai_service)

    with tab2:
        render_freshness_diagnostic_tab(ai_service)

    with tab3:
        render_hygiene_compliance_tab(ai_service)

    with tab4:
        render_recipe_assistant_tab(ai_service)

    with tab5:
        render_meal_planner_tab(ai_service)

if __name__ == "__main__":
    main()
