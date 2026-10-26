"""
Custom CSS and visual stylings for Food Verse AI.
Features modern glassmorphism, glowing emerald/culinary badges, and polished metric cards.
"""

import streamlit as st

def inject_custom_styles():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top Hero Header Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 95, 70, 0.3) 50%, rgba(17, 24, 39, 0.9) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(8px);
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #10B981, #34D399, #6EE7B7, #FBBF24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            padding-bottom: 6px;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            color: #9CA3AF;
            font-size: 1.05rem;
            margin-top: 4px;
            font-weight: 400;
        }

        /* Status & Capability Badges */
        .badge-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 12px;
        }

        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid transparent;
        }

        .badge-emerald {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border-color: rgba(16, 185, 129, 0.3);
        }

        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border-color: rgba(245, 158, 11, 0.3);
        }

        .badge-rose {
            background: rgba(244, 63, 94, 0.15);
            color: #FB7185;
            border-color: rgba(244, 63, 94, 0.3);
        }

        .badge-cyan {
            background: rgba(6, 182, 212, 0.15);
            color: #67E8F9;
            border-color: rgba(6, 182, 212, 0.3);
        }

        .badge-purple {
            background: rgba(168, 85, 247, 0.15);
            color: #C084FC;
            border-color: rgba(168, 85, 247, 0.3);
        }

        /* Glassmorphism Card Container */
        .glass-card {
            background: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: border-color 0.2s ease, transform 0.2s ease;
        }

        .glass-card:hover {
            border-color: rgba(16, 185, 129, 0.4);
        }

        .glass-card-accent {
            border-left: 4px solid #10B981;
        }

        .card-header-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #F3F4F6;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Metric Grid & Metric Cards */
        .metric-card {
            background: rgba(31, 41, 55, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #10B981;
            margin: 4px 0;
            font-family: 'JetBrains Mono', monospace;
        }

        .metric-label {
            font-size: 0.82rem;
            color: #9CA3AF;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }

        .metric-sub {
            font-size: 0.75rem;
            color: #6B7280;
            margin-top: 2px;
        }

        /* Freshness & Spoilage Alert Callouts */
        .fresh-callout {
            border-left: 5px solid #10B981;
            background: rgba(16, 185, 129, 0.08);
            border-radius: 8px;
            padding: 14px 18px;
            margin: 12px 0;
        }

        .moderate-callout {
            border-left: 5px solid #F59E0B;
            background: rgba(245, 158, 11, 0.08);
            border-radius: 8px;
            padding: 14px 18px;
            margin: 12px 0;
        }

        .spoiled-callout {
            border-left: 5px solid #EF4444;
            background: rgba(239, 68, 68, 0.08);
            border-radius: 8px;
            padding: 14px 18px;
            margin: 12px 0;
        }

        /* Streamlit Tab Enhancements */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(17, 24, 39, 0.5);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .stTabs [data-baseweb="tab"] {
            padding: 8px 18px;
            font-weight: 600;
            border-radius: 8px;
            color: #9CA3AF;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(16, 185, 129, 0.15) !important;
            color: #34D399 !important;
            border-bottom: 2px solid #10B981 !important;
        }

        /* Step cards for recipes and meal plans */
        .step-bubble {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            background: #10B981;
            color: #064E3B;
            border-radius: 50%;
            font-weight: 800;
            font-size: 0.85rem;
            margin-right: 10px;
        }

        /* Violation Table Pill */
        .severity-critical {
            background: #450A0A;
            color: #F87171;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
            display: inline-block;
        }
        .severity-major {
            background: #451A03;
            color: #FB923C;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
            display: inline-block;
        }
        .severity-minor {
            background: #3B2E05;
            color: #FACC15;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)
