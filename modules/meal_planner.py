"""
Tab 5: Personalized Meal Planner (Epic 5)
Computes BMR/TDEE caloric targets using the Mifflin-St Jeor formula,
generates an adaptive 7-day meal schedule, and produces an automated categorized grocery shopping list.
"""

import json
import streamlit as st

from utils.charts import create_weekly_meal_chart

def calculate_bmr_tdee(
    age: int,
    gender: str,
    weight_kg: float,
    height_cm: float,
    activity_multiplier: float,
    goal: str
) -> tuple[float, float, int, dict]:
    """
    Computes BMR using the Mifflin-St Jeor equation, TDEE, goal-adjusted calories,
    and macronutrient gram targets.
    """
    # Mifflin-St Jeor
    if gender == "Male":
        bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + 5.0
    else:
        bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) - 161.0

    tdee = bmr * activity_multiplier

    # Goal adjustment
    if "Fat Loss" in goal:
        target_kcal = int(tdee - 450)
    elif "Muscle" in goal:
        target_kcal = int(tdee + 350)
    else:  # Maintenance / Recomp
        target_kcal = int(tdee)

    target_kcal = max(1200, target_kcal)

    # Macro distribution (Protein: 30%, Carbs: 45%, Fat: 25% or goal-adjusted)
    if "Muscle" in goal:
        p_ratio, c_ratio, f_ratio = 0.35, 0.40, 0.25
    elif "Fat Loss" in goal:
        p_ratio, c_ratio, f_ratio = 0.35, 0.35, 0.30
    else:
        p_ratio, c_ratio, f_ratio = 0.30, 0.45, 0.25

    protein_g = int((target_kcal * p_ratio) / 4)
    carbs_g = int((target_kcal * c_ratio) / 4)
    fats_g = int((target_kcal * f_ratio) / 9)

    return bmr, tdee, target_kcal, {"protein": protein_g, "carbs": carbs_g, "fats": fats_g}

def render_meal_planner_tab(ai_service):
    st.markdown("""
        <div class="glass-card glass-card-accent">
            <div class="card-header-title">
                📅 Personalized 7-Day Meal Planner & Grocery Hub (Epic 5)
            </div>
            <p style="color: #9CA3AF; margin-bottom: 0;">
                Clinical bio-energetics engine calculating Basal Metabolic Rate (BMR) & Total Daily Energy Expenditure (TDEE).
                Generates a customized 7-day culinary roadmap with a synchronized supermarket grocery list.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_profile, col_plan = st.columns([1, 1.3], gap="medium")

    with col_profile:
        st.markdown("##### 👤 Step 1: User Biometrics & Dietary Profile")

        # Quick preset personas
        persona_choice = st.selectbox(
            "Quick Load Archetype Profile:",
            [
                "Custom User Input",
                "Alex (28M, 78kg, Gym Hypertrophy, High Protein)",
                "Sarah (32F, 64kg, Fat Loss / Deficit, Mediterranean)",
                "David (46M, 84kg, Diabetic-Friendly, Low Glycemic)"
            ],
            key="mp_archetype_select"
        )

        # Default values based on choice
        def_age, def_gender, def_wt, def_ht = 28, "Male", 75.0, 178.0
        def_act, def_diet, def_goal = "Moderately Active (Moderate exercise 3-5 days/wk)", "Standard Balanced", "Lean Recomposition / Maintenance"

        if "Alex" in persona_choice:
            def_age, def_gender, def_wt, def_ht = 28, "Male", 78.0, 182.0
            def_act = "Very Active (Hard training 6-7 days/wk)"
            def_diet = "High Protein"
            def_goal = "Muscle Hypertrophy / Clean Surplus (+350 kcal)"
        elif "Sarah" in persona_choice:
            def_age, def_gender, def_wt, def_ht = 32, "Female", 64.0, 166.0
            def_act = "Lightly Active (Light exercise 1-3 days/wk)"
            def_diet = "Mediterranean"
            def_goal = "Fat Loss / Caloric Deficit (-450 kcal)"
        elif "David" in persona_choice:
            def_age, def_gender, def_wt, def_ht = 46, "Male", 84.0, 175.0
            def_act = "Sedentary (Little or no exercise)"
            def_diet = "Diabetic-Friendly / Low Glycemic"
            def_goal = "Lean Recomposition / Maintenance"

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            age = st.number_input("Age (Years):", min_value=16, max_value=95, value=def_age, key="mp_age")
            gender = st.selectbox("Biological Sex:", ["Male", "Female"], index=0 if def_gender == "Male" else 1, key="mp_gender")
            weight_kg = st.number_input("Weight (kg):", min_value=35.0, max_value=200.0, value=def_wt, step=0.5, key="mp_wt")
        with b_c2:
            height_cm = st.number_input("Height (cm):", min_value=120.0, max_value=225.0, value=def_ht, step=1.0, key="mp_ht")
            goal = st.selectbox(
                "Fitness / Body Goal:",
                [
                    "Fat Loss / Caloric Deficit (-450 kcal)",
                    "Muscle Hypertrophy / Clean Surplus (+350 kcal)",
                    "Lean Recomposition / Maintenance"
                ],
                index=0 if "Fat Loss" in def_goal else (1 if "Muscle" in def_goal else 2),
                key="mp_goal"
            )
            diet_type = st.selectbox(
                "Dietary Regimen:",
                [
                    "Standard Balanced", "High Protein", "Mediterranean", "Diabetic-Friendly / Low Glycemic",
                    "Vegan", "Vegetarian", "Pescatarian", "Keto / Very Low Carb", "Gluten-Free"
                ],
                index=["Standard Balanced", "High Protein", "Mediterranean", "Diabetic-Friendly / Low Glycemic", "Vegan", "Vegetarian", "Pescatarian", "Keto / Very Low Carb", "Gluten-Free"].index(def_diet) if def_diet in ["Standard Balanced", "High Protein", "Mediterranean", "Diabetic-Friendly / Low Glycemic", "Vegan", "Vegetarian", "Pescatarian", "Keto / Very Low Carb", "Gluten-Free"] else 0,
                key="mp_diet"
            )

        activity_opts = {
            "Sedentary (Little or no exercise)": 1.2,
            "Lightly Active (Light exercise 1-3 days/wk)": 1.375,
            "Moderately Active (Moderate exercise 3-5 days/wk)": 1.55,
            "Very Active (Hard training 6-7 days/wk)": 1.725,
            "Extra Active (Intense athlete / physical job)": 1.9
        }
        activity_label = st.selectbox(
            "Physical Activity Level:",
            list(activity_opts.keys()),
            index=list(activity_opts.keys()).index(def_act) if def_act in activity_opts else 2,
            key="mp_activity"
        )
        act_mult = activity_opts[activity_label]

        # Bio-energetic Calculations
        bmr, tdee, target_kcal, macros = calculate_bmr_tdee(
            age=age,
            gender=gender,
            weight_kg=weight_kg,
            height_cm=height_cm,
            activity_multiplier=act_mult,
            goal=goal
        )

        st.markdown(f"""
            <div style="background: rgba(31, 41, 55, 0.6); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 14px; margin-top: 12px;">
                <div style="color: #34D399; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">
                    🧬 Clinical Energy Expenditure:
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #D1D5DB;">
                    <span><b>BMR (Basal):</b> {int(bmr)} kcal</span>
                    <span><b>TDEE (Daily):</b> {int(tdee)} kcal</span>
                    <span style="color: #10B981; font-weight: 700;"><b>Target:</b> {target_kcal} kcal/day</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #9CA3AF; margin-top: 6px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
                    <span>🍗 <b>Protein:</b> {macros['protein']}g</span>
                    <span>🍞 <b>Carbs:</b> {macros['carbs']}g</span>
                    <span>🥑 <b>Fats:</b> {macros['fats']}g</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        generate_plan_btn = st.button("🚀 Generate Adaptive 7-Day Meal Schedule", type="primary", use_container_width=True, key="btn_generate_meal_plan")

    with col_plan:
        st.markdown("##### 🍱 Step 2: Adaptive Schedule & Automated Grocery Hub")

        result_key = "cached_meal_planner_result"

        if generate_plan_btn:
            with st.spinner("Synthesizing 7-day culinary roadmap and clustering grocery staples..."):
                profile_payload = {
                    "age": age,
                    "gender": gender,
                    "weight_kg": weight_kg,
                    "height_cm": height_cm,
                    "activity_level": activity_label,
                    "fitness_goal": goal,
                    "dietary_constraint": diet_type
                }
                plan_result = ai_service.generate_meal_plan(
                    profile=profile_payload,
                    bmr=bmr,
                    tdee=tdee,
                    target_kcal=target_kcal,
                    macro_targets=macros
                )
                st.session_state[result_key] = plan_result

        if result_key in st.session_state:
            plan = st.session_state[result_key]

            approach = plan.get("dietary_approach", f"{diet_type} Plan")
            schedule = plan.get("daily_schedule", {})
            groceries = plan.get("grocery_list", {})
            coaching = plan.get("dietitian_coaching_notes", "Maintain hydration throughout the day.")

            st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #10B981;">{approach}</h4>
                        <span class="pill-badge badge-emerald">🎯 Target: {target_kcal} kcal/day</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Chart of 7 days
            daily_cals = {day: schedule[day].get("calories", target_kcal) for day in schedule}
            st.plotly_chart(create_weekly_meal_chart(daily_cals, target_kcal), use_container_width=True)

            # Tabs for Days vs Grocery List
            subtab_days, subtab_grocery = st.tabs(["📅 7-Day Meal Schedule", "🛒 Automated Grocery Shopping List"])

            with subtab_days:
                for day_name, day_info in schedule.items():
                    with st.expander(f"📌 {day_name} (Target: ~{day_info.get('calories', target_kcal)} kcal)", expanded=(day_name == "Monday")):
                        st.markdown(f"**🍳 Breakfast:** {day_info.get('breakfast', '')}")
                        st.markdown(f"**🥗 Lunch:** {day_info.get('lunch', '')}")
                        st.markdown(f"**🍲 Dinner:** {day_info.get('dinner', '')}")
                        st.markdown(f"**🍎 Snack / Fuel:** {day_info.get('snack', '')}")

            with subtab_grocery:
                st.markdown("###### 🛒 Weekly Supermarket Shopping Checklist:")
                for category, items in groceries.items():
                    st.markdown(f"**{category}:**")
                    cols = st.columns(2)
                    for idx, itm in enumerate(items):
                        with cols[idx % 2]:
                            st.checkbox(f"{itm}", value=False, key=f"chk_{category}_{idx}")

            # Coaching Notes
            st.markdown(f"""
                <div class="glass-card" style="margin-top: 14px;">
                    <b style="color: #F59E0B;">🩺 Sports Nutritionist Behavioral Strategy:</b>
                    <p style="color: #D1D5DB; font-size: 0.88rem; margin: 4px 0 0 0;">{coaching}</p>
                </div>
            """, unsafe_allow_html=True)

            # Export Full Plan
            plan_export_text = f"# Food Verse AI - 7-Day Personalized Meal Plan\n\n"
            plan_export_text += f"**Dietary Strategy:** {approach}\n**Daily Target:** {target_kcal} kcal (Protein: {macros['protein']}g, Carbs: {macros['carbs']}g, Fats: {macros['fats']}g)\n\n"
            plan_export_text += "## 7-Day Schedule:\n"
            for d_name, d_val in schedule.items():
                plan_export_text += f"\n### {d_name} (~{d_val.get('calories', target_kcal)} kcal)\n"
                plan_export_text += f"- Breakfast: {d_val.get('breakfast')}\n"
                plan_export_text += f"- Lunch: {d_val.get('lunch')}\n"
                plan_export_text += f"- Dinner: {d_val.get('dinner')}\n"
                plan_export_text += f"- Snack: {d_val.get('snack')}\n"
            plan_export_text += "\n## Grocery Shopping List:\n"
            for c_name, c_itms in groceries.items():
                plan_export_text += f"\n### {c_name}\n"
                for c_itm in c_itms:
                    plan_export_text += f"- [ ] {c_itm}\n"

            st.download_button(
                "📥 Export 7-Day Plan & Grocery Checklist (Markdown)",
                data=plan_export_text,
                file_name="foodverse_7day_meal_plan.md",
                mime="text/markdown",
                key="dl_meal_plan_md"
            )
        else:
            st.info("👈 Configure your biometrics and goals, then click 'Generate Adaptive 7-Day Meal Schedule'.")
