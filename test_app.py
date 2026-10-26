"""
Unit and integration tests for Multimodal Construction Intelligence Platform.
Validates imports, AI service fallback, chart builders, Indian currency formatters,
financial CapEx calculations, and material quantity surveying.
"""

import sys
import io

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def test_imports():
    print("Testing core imports...")
    import streamlit as st
    import plotly
    import plotly.graph_objects as go
    from PIL import Image
    import pandas as pd
    print("Core third-party imports successful!")

def test_local_utilities():
    print("Testing local utilities...")
    from utils.helpers import (
        format_inr,
        format_inr_indian_commas,
        get_safety_score_badge,
        get_severity_badge_class,
        parse_json_from_response,
        generate_audit_markdown_report
    )

    # Test Indian Rupee formatters
    assert "Cr" in format_inr(25000000), f"Expected Cr, got {format_inr(25000000)}"
    assert "Lakh" in format_inr(450000), f"Expected Lakh, got {format_inr(450000)}"
    assert "₹" in format_inr_indian_commas(12345678)
    print(f"Currency formatting passed: 2.5 Cr => {format_inr(25000000)}, 4.5 Lakh => {format_inr(450000)}")

    # Test Badges
    label_hi, cls_hi, _ = get_safety_score_badge(92)
    assert cls_hi == "badge-emerald"
    label_mid, cls_mid, _ = get_safety_score_badge(72)
    assert cls_mid == "badge-amber"
    label_lo, cls_lo, _ = get_safety_score_badge(45)
    assert cls_lo == "badge-rose"

    assert get_severity_badge_class("Critical") == "severity-critical"
    assert get_severity_badge_class("High") == "severity-high"

    # Test JSON parser
    raw_md = '```json\n{"safety_score": 85, "overall_status": "Compliant"}\n```'
    parsed = parse_json_from_response(raw_md)
    assert parsed.get("safety_score") == 85
    assert parsed.get("overall_status") == "Compliant"
    print("Helper utilities tests passed!")

def test_charts():
    print("Testing Plotly chart builders...")
    from utils.charts import (
        create_safety_gauge,
        create_crack_width_gauge,
        create_budget_capex_chart,
        create_materials_progress_chart,
        create_hazard_breakdown_donut
    )

    g1 = create_safety_gauge(78)
    assert g1 is not None
    g2 = create_crack_width_gauge(1.5, 0.2)
    assert g2 is not None
    c1 = create_budget_capex_chart(15.5, 7.2, 45.0)
    assert c1 is not None
    c2 = create_materials_progress_chart(350.0, 150.0, 1800.0, 800.0)
    assert c2 is not None
    d1 = create_hazard_breakdown_donut([{"severity": "Critical"}, {"severity": "High"}])
    assert d1 is not None
    print("All Plotly chart generations passed!")

def test_ai_service_demo():
    print("Testing Construction AI Service in Demonstration Mode...")
    from modules.ai_service import ConstructionAIService
    from modules.demo_data import DEMO_PPE_SITES, DEMO_CRACKS

    ai = ConstructionAIService(provider="demo")

    # Tab 1: PPE Audit
    ppe_res = ai.audit_site_safety_ppe(None, "Active High-Rise Slab Rebar & Concreting")
    assert "safety_score" in ppe_res
    assert "ppe_detection" in ppe_res
    assert len(ppe_res["ppe_detection"]) >= 4
    assert "site_hazards" in ppe_res
    print(f"PPE Audit Test Passed: Score={ppe_res['safety_score']}, Status={ppe_res['overall_status']}")

    # Tab 2: Crack Diagnostic
    crack_res = ai.diagnose_crack_structural(None, "Structural Shear Crack at Beam-Column Joint")
    assert "defect_type" in crack_res
    assert "engineering_repairs" in crack_res
    assert len(crack_res["engineering_repairs"]) >= 2
    assert "estimated_width_mm" in crack_res
    print(f"Crack Diagnostic Test Passed: Defect={crack_res['defect_type']}, Width={crack_res['estimated_width_mm']}mm")

    # Tab 4: Assistant Chat
    chat_reply_code = ai.chat_construction_assistant([{"role": "user", "content": "What are permissible crack widths in IS 456?"}])
    assert "IS 456" in chat_reply_code
    assert "0.30 mm" in chat_reply_code

    chat_reply_wind = ai.chat_construction_assistant([{"role": "user", "content": "What is the tower crane wind speed cutoff?"}])
    assert "38 km/h" in chat_reply_wind
    print("Chat Assistant Knowledge Retrieval Passed!")

def test_planning_calculations():
    print("Testing Planning & Valuation Calculations...")
    from modules.planning_valuation import BENCHMARK_RATES, TIER_MULTIPLIERS, SPEC_GRADE_MULTIPLIER

    built_up_sqft = 100000
    struct_info = BENCHMARK_RATES["Residential High-Rise (G+20)"]
    tier_info = TIER_MULTIPLIERS["Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Hyderabad)"]
    grade_factor = SPEC_GRADE_MULTIPLIER["Executive / Premium Grade"]

    unit_cost_sqft = struct_info["base_cost_sqft"] * tier_info["cost_factor"] * grade_factor
    total_budget = built_up_sqft * unit_cost_sqft
    capex_incurred = total_budget * 0.50

    assert total_budget > 250000000, f"Expected budget > 25 Cr, got {total_budget}"
    assert capex_incurred == total_budget * 0.5

    # Steel & Cement
    steel_mt = (built_up_sqft * struct_info["steel_kg_sqft"]) / 1000.0
    cement_bags = built_up_sqft * struct_info["cement_bags_sqft"]
    assert steel_mt > 300.0, f"Expected steel > 300 MT, got {steel_mt}"
    assert cement_bags > 35000, f"Expected cement > 35,000 bags, got {cement_bags}"

    print(f"Valuation & Quantity Surveying Test Passed: Budget=₹{total_budget/1e7:.2f} Cr, Steel={steel_mt:.1f} MT, Cement={cement_bags:,.0f} bags")

if __name__ == "__main__":
    test_imports()
    test_local_utilities()
    test_charts()
    test_ai_service_demo()
    test_planning_calculations()
    print("\n========================================================")
    print("✅ ALL CAPSTONE PROJECT 1 UNIT & INTEGRATION TESTS PASSED!")
    print("========================================================")
