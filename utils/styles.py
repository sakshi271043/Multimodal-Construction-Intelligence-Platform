"""
Custom CSS and visual styling for Multimodal Construction Intelligence Platform.
Features industrial glassmorphism, safety amber accents, hazard status pills, and engineering cards.
"""

import streamlit as st

def inject_custom_styles():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top Hero Header Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.16) 0%, rgba(217, 119, 6, 0.22) 40%, rgba(17, 24, 39, 0.95) 100%);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #F59E0B, #FBBF24, #FCD34D, #FB923C);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            padding-bottom: 6px;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            color: #94A3B8;
            font-size: 1.02rem;
            margin-top: 4px;
            font-weight: 400;
            line-height: 1.5;
        }

        /* Status & Capability Badges */
        .badge-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 14px;
        }

        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 13px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid transparent;
            letter-spacing: 0.2px;
        }

        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border-color: rgba(245, 158, 11, 0.35);
        }

        .badge-emerald {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border-color: rgba(16, 185, 129, 0.35);
        }

        .badge-rose {
            background: rgba(244, 63, 94, 0.18);
            color: #FB7185;
            border-color: rgba(244, 63, 94, 0.4);
        }

        .badge-cyan {
            background: rgba(6, 182, 212, 0.15);
            color: #67E8F9;
            border-color: rgba(6, 182, 212, 0.35);
        }

        .badge-purple {
            background: rgba(168, 85, 247, 0.15);
            color: #C084FC;
            border-color: rgba(168, 85, 247, 0.35);
        }

        .badge-slate {
            background: rgba(148, 163, 184, 0.12);
            color: #CBD5E1;
            border-color: rgba(148, 163, 184, 0.25);
        }

        /* Glassmorphism Card Container */
        .glass-card {
            background: rgba(17, 24, 39, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        .glass-card-accent {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
        }

        /* Metric Box with Colored Accents */
        .metric-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 16px 18px;
            text-align: left;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: #F59E0B;
        }

        .metric-card.emerald::before { background: #10B981; }
        .metric-card.rose::before { background: #EF4444; }
        .metric-card.cyan::before { background: #06B6D4; }
        .metric-card.purple::before { background: #8B5CF6; }

        .metric-label {
            font-size: 0.78rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .metric-value {
            font-size: 1.7rem;
            font-weight: 800;
            color: #F8FAFC;
            margin: 4px 0;
            font-family: 'JetBrains Mono', monospace;
        }

        .metric-sub {
            font-size: 0.78rem;
            color: #64748B;
        }

        /* Severity Tags */
        .severity-critical {
            background: rgba(239, 68, 68, 0.2);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.5);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }

        .severity-high {
            background: rgba(249, 115, 22, 0.2);
            color: #FB923C;
            border: 1px solid rgba(249, 115, 22, 0.5);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }

        .severity-medium {
            background: rgba(234, 179, 8, 0.2);
            color: #FACC15;
            border: 1px solid rgba(234, 179, 8, 0.5);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }

        .severity-low {
            background: rgba(16, 185, 129, 0.2);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.5);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }

        /* Weather Alert Banner */
        .weather-alert-box {
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            border-left: 5px solid;
            background: rgba(17, 24, 39, 0.85);
        }

        .weather-alert-box.wind {
            border-color: #F59E0B;
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.12), rgba(17, 24, 39, 0.8));
        }

        .weather-alert-box.rain {
            border-color: #3B82F6;
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.12), rgba(17, 24, 39, 0.8));
        }

        .weather-alert-box.heat {
            border-color: #EF4444;
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.12), rgba(17, 24, 39, 0.8));
        }

        .weather-alert-box.normal {
            border-color: #10B981;
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.12), rgba(17, 24, 39, 0.8));
        }

        /* Inspection Row Table */
        .ppe-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 6px;
            margin-top: 10px;
        }

        .ppe-table th {
            color: #94A3B8;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .ppe-table td {
            background: rgba(15, 23, 42, 0.6);
            padding: 10px 12px;
            font-size: 0.85rem;
            color: #E2E8F0;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }

        .ppe-table tr td:first-child {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
        }

        .ppe-table tr td:last-child {
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }

        /* Chat Assistant Styling */
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 14px;
        }

        .chat-bubble-user {
            align-self: flex-end;
            background: #1E293B;
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #F8FAFC;
            border-radius: 14px 14px 2px 14px;
            padding: 12px 16px;
            max-width: 80%;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .chat-bubble-ai {
            align-self: flex-start;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #E2E8F0;
            border-radius: 14px 14px 14px 2px;
            padding: 14px 18px;
            max-width: 85%;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* Code block styling */
        pre, code {
            font-family: 'JetBrains Mono', monospace !important;
        }
        </style>
    """, unsafe_allow_html=True)
