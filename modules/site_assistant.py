"""
Tab 4: Daily Site Assistant & Weather-Aware Advisory Module (Epic 5).
Weather condition selector (High Wind, Heavy Rain, Extreme Heat, Normal, Fog) displaying
dynamic civil safety alerts (crane cutoff limits, electrical safety, concrete curing protocols)
and an interactive multi-turn construction engineering chatbot.
"""

import streamlit as st

from modules.ai_service import ConstructionAIService
from modules.demo_data import DEMO_WEATHER_PROTOCOLS

def render_site_assistant_tab(ai_service: ConstructionAIService):
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #F8FAFC; margin-bottom: 4px; font-weight: 700;">
                🌦️ Daily Site Assistant & Weather-Aware Safety Advisory
            </h2>
            <div style="color: #94A3B8; font-size: 0.95rem;">
                Dynamic environmental risk mitigations (IS 875 Wind Cutoffs, Monsoon Grounding, Hydration Cracking)
                paired with an Interactive Multi-Turn Construction Engineering Chatbot.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. Weather Advisory Section
    st.markdown("### 🌤️ 1. Active Environmental Conditions & Dynamic Safety Protocols")

    col_w_select, col_w_summary = st.columns([1, 2], gap="medium")

    with col_w_select:
        weather_choice = st.selectbox(
            "Select Site Atmospheric Condition:",
            list(DEMO_WEATHER_PROTOCOLS.keys()),
            index=0
        )
        weather_data = DEMO_WEATHER_PROTOCOLS[weather_choice]

        st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 20px 14px;">
                <span style="font-size: 2.8rem;">{weather_data['icon']}</span>
                <h4 style="margin: 6px 0 2px 0; color: #F8FAFC;">{weather_choice}</h4>
                <span class="pill-badge {'badge-rose' if weather_data['severity']=='High' else 'badge-amber' if weather_data['severity']=='Medium' else 'badge-emerald'}">
                    {weather_data['severity'].upper()} RISK FACTOR
                </span>
            </div>
        """, unsafe_allow_html=True)

    with col_w_summary:
        st.markdown(f"""
            <div class="weather-alert-box {weather_data['style_class']}">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1.4rem;">{weather_data['icon']}</span>
                    <h3 style="margin: 0; color: #F8FAFC; font-size: 1.15rem; font-weight: 800; letter-spacing: 0.3px;">
                        {weather_data['headline']}
                    </h3>
                </div>
                <div style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.6;">
                    Mandatory field directives based on <b>IS 875 (Part 3)</b>, <b>IS 456 (Clause 14)</b>, and <b>OSHA 1926 Subpart CC</b>:
                </div>
            </div>
        """, unsafe_allow_html=True)

        for proto in weather_data["protocols"]:
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; border-left: 3px solid #F59E0B; font-size: 0.88rem; color: #E2E8F0; line-height: 1.5;">
                    {proto}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Interactive Multi-Turn Construction Engineering Chatbot
    st.markdown("### 🤖 2. Interactive Construction Engineering Assistant")
    st.markdown("""
        <div style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 14px;">
            Consult with our Senior Chartered Structural Engineer & Site Safety Director.
            Ask questions regarding <b>IS 456 permissible crack limits</b>, <b>OSHA wind speed cutoffs</b>,
            <b>concrete mix design</b>, or <b>structural retrofit techniques</b>.
        </div>
    """, unsafe_allow_html=True)

    # Initialize chat history in session state
    if "construction_chat_history" not in st.session_state:
        st.session_state["construction_chat_history"] = [
            {
                "role": "assistant",
                "content": (
                    "**Greetings Engineer.** I am your Multimodal Construction Engineering & EHS Director. "
                    "I am actively monitoring site conditions and can assist you with structural crack remediation, "
                    "IS 456 / IS 1893 seismic compliance, OSHA safety regulations, crane wind thresholds, "
                    "or concrete mix quantity calculations. How can I assist your site today?"
                )
            }
        ]

    # Quick Prompt Chips
    st.markdown("##### 💡 Quick Technical Inquiries:")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    quick_query = None
    with q_col1:
        if st.button("📏 IS 456 Crack Widths", use_container_width=True):
            quick_query = "What are the permissible crack widths as per IS 456:2000 for mild, moderate, and severe exposures?"
    with q_col2:
        if st.button("💨 Tower Crane Wind Limit", use_container_width=True):
            quick_query = "What wind speed cutoff halts tower crane operations under OSHA and IS 875?"
    with q_col3:
        if st.button("🧪 Epoxy vs PU Injection", use_container_width=True):
            quick_query = "Explain structural epoxy injection versus hydrophilic polyurethane grouting for crack repair."
    with q_col4:
        if st.button("🧱 Cement Bags in M25", use_container_width=True):
            quick_query = "How many bags of cement and kg of steel are needed for an M25 concrete slab design?"

    # Render Existing Chat History
    chat_box = st.container()
    with chat_box:
        for msg in st.session_state["construction_chat_history"]:
            with st.chat_message(msg["role"], avatar="👷‍♂️" if msg["role"] == "user" else "🏗️"):
                st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Enter your structural engineering or site safety question...")

    # Process either quick query or typed input
    prompt_to_send = quick_query or user_input

    if prompt_to_send:
        # Append User Message
        st.session_state["construction_chat_history"].append({
            "role": "user",
            "content": prompt_to_send
        })

        # Display user message immediately
        with st.chat_message("user", avatar="👷‍♂️"):
            st.markdown(prompt_to_send)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🏗️"):
            with st.spinner("Analyzing civil engineering codes & site parameters..."):
                reply = ai_service.chat_construction_assistant(
                    messages=st.session_state["construction_chat_history"],
                    weather_context=weather_choice
                )
                st.markdown(reply)

        # Append Assistant Response
        st.session_state["construction_chat_history"].append({
            "role": "assistant",
            "content": reply
        })

    # Clear Chat Button
    c_clear1, c_clear2 = st.columns([4, 1])
    with c_clear2:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state["construction_chat_history"] = [
                {
                    "role": "assistant",
                    "content": "Chat history cleared. How may I assist your engineering queries?"
                }
            ]
            st.rerun()
