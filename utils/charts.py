"""
Plotly charting routines for Food Verse AI:
Macro Donut, Health Score Gauges, Freshness Meters, and Compliance Gauges.
"""

import plotly.graph_objects as go
from typing import Dict, Any

DEFAULT_LAYOUT_KWARGS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F3F4F6", family="Plus Jakarta Sans, sans-serif"),
)

def create_macro_donut_chart(protein_g: float, carbs_g: float, fat_g: float) -> go.Figure:
    """
    Renders an interactive high-contrast macro donut chart:
    Protein (4 kcal/g), Carbs (4 kcal/g), Fat (9 kcal/g).
    """
    # Calculate calories per macro
    p_cal = max(0.0, float(protein_g)) * 4.0
    c_cal = max(0.0, float(carbs_g)) * 4.0
    f_cal = max(0.0, float(fat_g)) * 9.0
    total_cal = p_cal + c_cal + f_cal

    labels = ["Protein", "Carbohydrates", "Fats"]
    values = [protein_g, carbs_g, fat_g]
    colors = ["#10B981", "#3B82F6", "#F59E0B"]  # Emerald, Blue, Amber

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#111827", width=2)),
            textinfo="label+percent",
            hoverinfo="label+value+percent",
            hovertemplate="<b>%{label}</b><br>%{value:.1f}g (%{percent})<extra></extra>",
            textfont=dict(size=12, color="#FFFFFF")
        )
    ])

    fig.update_layout(
        **DEFAULT_LAYOUT_KWARGS,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#9CA3AF")
        ),
        annotations=[
            dict(
                text=f"<b>{int(total_cal)}</b><br><span style='font-size:11px;color:#9CA3AF'>Est. Macro kcal</span>",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False,
                font=dict(color="#FFFFFF")
            )
        ],
        height=280
    )
    return fig

def create_score_gauge(score: int, title: str = "Health Score", max_score: int = 100) -> go.Figure:
    """
    Creates a radial gauge meter for Health Score or Freshness Index.
    """
    if score >= 80:
        bar_color = "#10B981"
    elif score >= 60:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': f"<b>{title}</b>", 'font': {'size': 14, 'color': '#9CA3AF'}},
        number={'suffix': f"/{max_score}", 'font': {'size': 26, 'color': '#FFFFFF', 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, max_score], 'tickwidth': 1, 'tickcolor': "#374151"},
            'bar': {'color': bar_color, 'thickness': 0.28},
            'bgcolor': "rgba(31, 41, 55, 0.5)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': bar_color, 'width': 3},
                'thickness': 0.8,
                'value': score
            }
        }
    ))

    fig.update_layout(
        **DEFAULT_LAYOUT_KWARGS,
        height=220,
        margin=dict(l=15, r=15, t=35, b=10)
    )
    return fig

def create_compliance_gauge(compliance_score: int) -> go.Figure:
    """
    Creates a Kitchen Hygiene compliance gauge with FDA/HACCP tiers.
    """
    if compliance_score >= 85:
        color = "#10B981"
        tier = "Grade A"
    elif compliance_score >= 70:
        color = "#F59E0B"
        tier = "Grade B"
    else:
        color = "#EF4444"
        tier = "Fail / Action"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=compliance_score,
        delta={'reference': 85, 'increasing': {'color': '#10B981'}, 'decreasing': {'color': '#EF4444'}},
        title={'text': f"<b>Hygiene Compliance ({tier})</b>", 'font': {'size': 14, 'color': '#9CA3AF'}},
        number={'suffix': "%", 'font': {'size': 28, 'color': color, 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#4B5563"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "rgba(17, 24, 39, 0.8)",
            'steps': [
                {'range': [0, 69], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [70, 84], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
            ]
        }
    ))

    fig.update_layout(
        **DEFAULT_LAYOUT_KWARGS,
        height=220,
        margin=dict(l=15, r=15, t=35, b=10)
    )
    return fig

def create_weekly_meal_chart(daily_calories: Dict[str, int], target_kcal: int) -> go.Figure:
    """
    Renders bar chart comparing 7-day scheduled calories against daily target.
    """
    days = list(daily_calories.keys())
    cals = list(daily_calories.values())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=days,
        y=cals,
        name="Planned Intake (kcal)",
        marker=dict(color="#10B981", line=dict(color="#34D399", width=1.5)),
        hovertemplate="%{x}: <b>%{y} kcal</b><extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=days,
        y=[target_kcal] * len(days),
        mode="lines",
        name="Target TDEE",
        line=dict(color="#F59E0B", width=2, dash="dash"),
        hovertemplate="Target: %{y} kcal<extra></extra>"
    ))

    fig.update_layout(
        **DEFAULT_LAYOUT_KWARGS,
        title=dict(text="7-Day Caloric Allocation vs Target", font=dict(size=14, color="#E5E7EB")),
        xaxis=dict(title="", tickfont=dict(color="#9CA3AF")),
        yaxis=dict(title="Calories (kcal)", tickfont=dict(color="#9CA3AF"), gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=260,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
