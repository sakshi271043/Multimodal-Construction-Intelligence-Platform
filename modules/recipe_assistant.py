"""
Tab 4: Smart Kitchen Recipe Assistant (Epic 4)
Inventory-driven recipe generation with cooking time, difficulty level,
step-by-step instructions, ingredient substitutions, and zero-waste cooking tips.
"""

import json
import streamlit as st

def render_recipe_assistant_tab(ai_service):
    st.markdown("""
        <div class="glass-card glass-card-accent">
            <div class="card-header-title">
                🍳 Smart Kitchen Recipe Assistant (Epic 4)
            </div>
            <p style="color: #9CA3AF; margin-bottom: 0;">
                Turn surplus ingredients and pantry staples into gourmet, nutritionally balanced recipes.
                Featuring smart ingredient substitution matrix, step-by-step chef instructions, and zero-waste hacks.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_pantry, col_recipes = st.columns([1, 1.2], gap="medium")

    with col_pantry:
        st.markdown("##### 🛒 Step 1: Available Pantry Inventory")

        # Quick preset pantry baskets
        basket_preset = st.selectbox(
            "Quick Load Curated Pantry Basket:",
            [
                "Custom Ingredients",
                "High-Protein Mediterranean Basket (Chicken, Quinoa, Broccoli, Garlic, Lemon, Olive Oil)",
                "Crispy Asian Stir-Fry Basket (Tofu, Bell Pepper, Broccoli, Ginger, Soy Sauce, Brown Rice)",
                "Rustic Italian Pantry (Pasta, Canned Tomatoes, Garlic, Basil, Parmesan, Olive Oil)"
            ],
            key="recipe_basket_preset"
        )

        default_items = []
        if "Mediterranean" in basket_preset:
            default_items = ["Chicken breast", "Broccoli", "Quinoa", "Olive oil", "Garlic", "Lemon"]
        elif "Asian" in basket_preset:
            default_items = ["Tofu", "Bell pepper", "Broccoli", "Soy sauce", "Garlic", "Ginger", "Brown rice"]
        elif "Italian" in basket_preset:
            default_items = ["Pasta", "Canned tomatoes", "Garlic", "Basil", "Parmesan", "Olive oil"]
        else:
            default_items = ["Eggs", "Spinach", "Avocado", "Sourdough bread", "Olive oil"]

        # Multiselect with tags & text area
        selected_ingredients = st.multiselect(
            "Select or Add Pantry Items:",
            options=[
                "Chicken breast", "Salmon fillet", "Ground beef", "Tofu", "Eggs",
                "Broccoli", "Spinach", "Bell pepper", "Zucchini", "Carrots", "Avocado",
                "Quinoa", "Brown rice", "Rolled oats", "Pasta", "Sweet potato",
                "Garlic", "Onion", "Ginger", "Lemon", "Olive oil", "Soy sauce", "Parmesan"
            ],
            default=default_items,
            key="pantry_multiselect"
        )

        custom_text_items = st.text_input(
            "Additional Ingredients (comma-separated):",
            placeholder="e.g. Greek yogurt, feta cheese, walnuts",
            key="pantry_text_custom"
        )

        all_ingredients = list(selected_ingredients)
        if custom_text_items:
            for item in custom_text_items.split(","):
                cleaned = item.strip()
                if cleaned and cleaned not in all_ingredients:
                    all_ingredients.append(cleaned)

        st.markdown("##### ⚙️ Culinary Preferences")
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            diet_pref = st.selectbox(
                "Dietary Constraint:",
                ["Any / Balanced", "High Protein", "Low Carb / Keto", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"],
                key="recipe_diet_pref"
            )
            meal_type = st.selectbox(
                "Meal Course:",
                ["Dinner", "Lunch", "Breakfast", "Post-Workout Snack"],
                key="recipe_meal_type"
            )
        with c_d2:
            max_cook_time = st.slider("Max Cook Time (Mins):", 15, 60, 35, step=5, key="recipe_max_time")
            skill_level = st.selectbox("Skill Level:", ["Beginner-Friendly", "Intermediate", "Master Chef"], key="recipe_skill_level")

        generate_btn = st.button("✨ Generate AI Chef Recipes", type="primary", use_container_width=True, key="btn_generate_recipes")

    with col_recipes:
        st.markdown("##### 🍽️ Step 2: Custom Formulated Recipes")

        result_key = "cached_recipe_assistant_result"

        if generate_btn:
            with st.spinner("Formulating optimal flavour profiles, cooking times, and zero-waste techniques..."):
                recipes = ai_service.generate_recipes(
                    pantry_items=all_ingredients,
                    dietary_preference=diet_pref,
                    meal_type=meal_type,
                    max_time_mins=max_cook_time,
                    skill_level=skill_level
                )
                st.session_state[result_key] = recipes

        if result_key in st.session_state:
            recipes = st.session_state[result_key]

            for i, r in enumerate(recipes):
                title = r.get("title", f"Gourmet Recipe {i+1}")
                cuisine = r.get("cuisine", "Global Kitchen")
                prep_time = r.get("prep_time", "15m")
                cook_time = r.get("cook_time", "20m")
                total_time = r.get("total_time", "35m")
                servings = r.get("servings", 2)
                diff = r.get("difficulty", "Easy")
                cals = r.get("calories_per_serving", 420)
                macros = r.get("macros", {})
                pantry_used = r.get("pantry_used", [])
                subs = r.get("substitutions", [])
                instructions = r.get("instructions", [])
                chef_tip = r.get("chef_pro_tip", "Rest before serving.")
                zero_waste = r.get("zero_waste_tip", "Compost vegetable trimmings.")

                st.markdown(f"""
                    <div class="glass-card" style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                            <div>
                                <h3 style="color: #10B981; margin: 0; font-size: 1.3rem;">{title}</h3>
                                <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 4px;">
                                    <span>🌍 {cuisine}</span> &nbsp;|&nbsp; 
                                    <span>⏱️ Total: <b>{total_time}</b> (Prep: {prep_time}, Cook: {cook_time})</span> &nbsp;|&nbsp;
                                    <span>👥 Serves: <b>{servings}</b></span>
                                </div>
                            </div>
                            <span class="pill-badge badge-amber">⚡ {diff}</span>
                        </div>
                        <div style="display: flex; gap: 12px; margin-top: 10px; background: rgba(31, 41, 55, 0.4); padding: 8px 12px; border-radius: 8px; font-size: 0.85rem;">
                            <span style="color: #F3F4F6;"><b>Energy:</b> {cals} kcal/serving</span>
                            <span style="color: #34D399;"><b>P:</b> {macros.get('protein', '35g')}</span>
                            <span style="color: #60A5FA;"><b>C:</b> {macros.get('carbs', '40g')}</span>
                            <span style="color: #FBBF24;"><b>F:</b> {macros.get('fat', '14g')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Used ingredients & substitutions
                with st.expander(f"🛒 Ingredients & Smart Substitutions - {title}", expanded=True):
                    st.markdown(f"**Pantry Items Utilized:** {', '.join(pantry_used)}")
                    if subs:
                        st.markdown("**🔄 Flexible Substitutions Matrix:**")
                        for sub in subs:
                            st.markdown(f"- {sub}")

                # Step-by-step instructions
                with st.expander(f"👨‍🍳 Step-by-Step Culinary Instructions ({len(instructions)} Steps)", expanded=True):
                    for step_idx, step_text in enumerate(instructions, 1):
                        st.markdown(f"""
                            <div style="display: flex; align-items: flex-start; margin-bottom: 8px;">
                                <div class="step-bubble">{step_idx}</div>
                                <div style="color: #E5E7EB; font-size: 0.9rem; line-height: 1.4;">{step_text}</div>
                            </div>
                        """, unsafe_allow_html=True)

                # Pro-tip & Zero-waste callout
                st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 3px solid #10B981; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 0.85rem;">
                        <b style="color: #34D399;">💡 Executive Chef Pro-Tip:</b><br/>
                        <span style="color: #D1D5DB;">{chef_tip}</span>
                    </div>
                    <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid #F59E0B; padding: 10px 14px; border-radius: 6px; margin-bottom: 24px; font-size: 0.85rem;">
                        <b style="color: #FBBF24;">🌱 Zero-Waste Sustainability Hack:</b><br/>
                        <span style="color: #D1D5DB;">{zero_waste}</span>
                    </div>
                """, unsafe_allow_html=True)

            # Export Recipes
            recipe_md = f"# Food Verse AI Generated Recipes\n\n"
            for r in recipes:
                recipe_md += f"## {r.get('title')}\n- Cuisine: {r.get('cuisine')}\n- Time: {r.get('total_time')}\n- Calories: {r.get('calories_per_serving')} kcal\n\n### Instructions:\n"
                for s_i, stp in enumerate(r.get("instructions", []), 1):
                    recipe_md += f"{s_i}. {stp}\n"
                recipe_md += f"\n**Chef Secret:** {r.get('chef_pro_tip')}\n\n---\n\n"

            st.download_button(
                "📥 Export Recipes (Markdown)",
                data=recipe_md,
                file_name="foodverse_chef_recipes.md",
                mime="text/markdown",
                key="dl_recipes_md"
            )
        else:
            st.info("👈 Select your available pantry items and click 'Generate AI Chef Recipes' to start cooking.")
