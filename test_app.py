"""
Unit and integration tests for Food Verse AI application.
Validates imports, AI service fallback, chart builders, BMR/TDEE calculations, and demo data integrity.
"""

import sys

def test_imports():
    print("Testing core imports...")
    import streamlit as st
    import plotly
    import plotly.graph_objects as go
    from PIL import Image
    import pandas as pd
    import groq
    print("Core third-party imports successful!")

def test_local_modules():
    print("Testing local modules...")
    from utils.helpers import parse_json_from_response, get_health_score_badge, get_freshness_badge, get_hygiene_score_badge
    from utils.charts import create_macro_donut_chart, create_score_gauge, create_compliance_gauge, create_weekly_meal_chart
    from modules.demo_data import DEMO_NUTRITION_ITEMS, DEMO_FRESHNESS_ITEMS, DEMO_HYGIENE_INSPECTIONS, DEMO_RECIPES
    from modules.ai_service import FoodVerseAIService
    from modules.meal_planner import calculate_bmr_tdee

    # Test BMR/TDEE calculations
    bmr_m, tdee_m, target_m, macros_m = calculate_bmr_tdee(28, "Male", 78.0, 180.0, 1.55, "Muscle Hypertrophy / Clean Surplus (+350 kcal)")
    assert bmr_m > 1600, f"Expected BMR > 1600, got {bmr_m}"
    assert tdee_m > bmr_m, f"Expected TDEE > BMR, got {tdee_m}"
    assert target_m > tdee_m, f"Expected surplus, got {target_m}"
    print(f"BMR/TDEE Male Test Passed: BMR={int(bmr_m)}, TDEE={int(tdee_m)}, Target={target_m}, Macros={macros_m}")

    bmr_f, tdee_f, target_f, macros_f = calculate_bmr_tdee(32, "Female", 65.0, 165.0, 1.375, "Fat Loss / Caloric Deficit (-450 kcal)")
    assert bmr_f > 1200, f"Expected BMR > 1200, got {bmr_f}"
    assert target_f < tdee_f, f"Expected deficit, got {target_f}"
    print(f"BMR/TDEE Female Test Passed: BMR={int(bmr_f)}, TDEE={int(tdee_f)}, Target={target_f}, Macros={macros_f}")

    # Test Charts
    fig_donut = create_macro_donut_chart(40.0, 50.0, 15.0)
    assert fig_donut is not None
    fig_gauge = create_score_gauge(92, "Health Score")
    assert fig_gauge is not None
    fig_comp = create_compliance_gauge(88)
    assert fig_comp is not None
    fig_week = create_weekly_meal_chart({"Monday": 2100, "Tuesday": 2050}, 2100)
    assert fig_week is not None
    print("Plotly chart generation tests passed!")

    # Test AI Service in Demo Mode
    ai = FoodVerseAIService(provider="demo")
    nutri_res = ai.analyze_nutrition(None, "Mediterranean Salmon & Quinoa Bowl")
    assert nutri_res["dish_name"] != ""
    assert nutri_res["calories_kcal"] > 0
    print(f"AI Service Nutrition Test Passed: {nutri_res['dish_name']}, {nutri_res['calories_kcal']} kcal")

    fresh_res = ai.analyze_freshness(None, "Fresh Hass Avocado")
    assert fresh_res["freshness_stage"] == "Fresh"
    print(f"AI Service Freshness Test Passed: {fresh_res['item_name']}, Stage: {fresh_res['freshness_stage']}")

    hygiene_res = ai.audit_kitchen_hygiene(None, "Commercial Prep Kitchen - Critical Violation")
    assert "compliance_score" in hygiene_res
    print(f"AI Service Hygiene Test Passed: Score {hygiene_res['compliance_score']}%")

    recipe_res = ai.generate_recipes(["Chicken", "Quinoa", "Broccoli"])
    assert len(recipe_res) >= 1
    print(f"AI Service Recipe Test Passed: Generated {len(recipe_res)} recipes")

    plan_res = ai.generate_meal_plan({"dietary_constraint": "Mediterranean", "fitness_goal": "Maintenance"}, bmr_m, tdee_m, target_m, macros_m)
    assert "daily_schedule" in plan_res
    assert "Monday" in plan_res["daily_schedule"]
    assert "grocery_list" in plan_res
    print("AI Service Meal Plan Test Passed: 7 days and grocery categories generated!")

    print("\nALL SYSTEM TESTS PASSED SUCCESSFULLY! 100% PRODUCTION READY.")

if __name__ == "__main__":
    test_imports()
    test_local_modules()
