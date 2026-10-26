"""
Plotly visualization builders for Multimodal Construction Intelligence Platform.
High-end dark-mode gauges, material progress bars, and hazard distribution charts.
"""

from typing import Dict, List, Optional
import plotly.graph_objects as go

DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F8FAFC", family="Plus Jakarta Sans, sans-serif")
)

def create_safety_gauge(score: int, title: str = "Site Safety Compliance Score") -> go.Figure:
    """
    Creates an industrial radial gauge for OSHA & IS 456 Safety Compliance (0-100).
    """
    if score >= 85:
        bar_color = "#10B981"
    elif score >= 65:
        bar_color = "#F59E0B"
    else:
        bar_color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#94A3B8'}},
        number={'suffix': "/100", 'font': {'size': 36, 'color': '#FFFFFF', 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569", 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "rgba(30, 41, 59, 0.7)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 65], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [65, 85], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': "#F59E0B", 'width': 3},
                'thickness': 0.8,
                'value': 85
            }
        }
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        height=240,
        margin=dict(l=25, r=25, t=40, b=15)
    )
    return fig

def create_crack_width_gauge(width_mm: float, exposure_limit: float = 0.3) -> go.Figure:
    """
    Creates a comparative crack width gauge with IS 456:2000 exposure limits.
    """
    max_val = max(5.0, round(width_mm * 1.5, 1))
    bar_color = "#10B981" if width_mm <= exposure_limit else ("#F59E0B" if width_mm <= 1.0 else "#EF4444")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=width_mm,
        delta={'reference': exposure_limit, 'increasing': {'color': "#EF4444"}, 'decreasing': {'color': "#10B981"}, 'suffix': " mm"},
        title={'text': f"Crack Width vs IS 456 Limit ({exposure_limit}mm)", 'font': {'size': 14, 'color': '#94A3B8'}},
        number={'suffix': " mm", 'font': {'size': 32, 'color': '#FFFFFF', 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, max_val], 'tickwidth': 1, 'tickcolor': '#475569'},
            'bar': {'color': bar_color, 'thickness': 0.32},
            'bgcolor': "rgba(30, 41, 59, 0.6)",
            'steps': [
                {'range': [0, exposure_limit], 'color': 'rgba(16, 185, 129, 0.2)'},
                {'range': [exposure_limit, 1.0], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [1.0, max_val], 'color': 'rgba(239, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 3},
                'thickness': 0.8,
                'value': exposure_limit
            }
        }
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        height=220,
        margin=dict(l=25, r=25, t=35, b=15)
    )
    return fig

def create_budget_capex_chart(budget_cr: float, capex_cr: float, completion_pct: float) -> go.Figure:
    """
    Visualizes CapEx Incurred vs Cost-to-Complete against Total Project Budget.
    """
    cost_to_complete = max(0.0, budget_cr - capex_cr)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['Project CapEx'],
        x=[capex_cr],
        name=f'CapEx Incurred ({completion_pct:.0f}%)',
        orientation='h',
        marker=dict(color='#F59E0B', line=dict(color='rgba(255,255,255,0.2)', width=1)),
        text=[f"₹ {capex_cr:.2f} Cr"],
        textposition='inside'
    ))
    fig.add_trace(go.Bar(
        y=['Project CapEx'],
        x=[cost_to_complete],
        name='Cost to Complete',
        orientation='h',
        marker=dict(color='#334155', line=dict(color='rgba(255,255,255,0.1)', width=1)),
        text=[f"₹ {cost_to_complete:.2f} Cr"],
        textposition='inside'
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        barmode='stack',
        height=150,
        title={'text': f"Financial Milestone: Total Budget ₹ {budget_cr:.2f} Cr", 'font': {'size': 14, 'color': '#94A3B8'}},
        xaxis=dict(title='Amount in ₹ Crores', gridcolor='rgba(255, 255, 255, 0.06)'),
        yaxis=dict(showticklabels=False),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def create_materials_progress_chart(steel_total_mt: float, steel_used_mt: float, cement_total_t: float, cement_used_t: float) -> go.Figure:
    """
    Comparative dual bar chart for Structural Steel (MT) and Cement (Tonnes).
    """
    categories = ['Structural Steel (MT)', 'Cement (Tonnes)']
    consumed = [round(steel_used_mt, 1), round(cement_used_t, 1)]
    remaining = [round(max(0, steel_total_mt - steel_used_mt), 1), round(max(0, cement_total_t - cement_used_t), 1)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=consumed,
        name='Incurred / Consumed',
        marker_color='#06B6D4',
        text=[f"{v:,}" for v in consumed],
        textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=categories,
        y=remaining,
        name='Remaining to Pour',
        marker_color='#475569',
        text=[f"{v:,}" for v in remaining],
        textposition='auto'
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        barmode='stack',
        height=260,
        title={'text': "Core Material Requirement Breakdown (CPWD Benchmark)", 'font': {'size': 14, 'color': '#94A3B8'}},
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.06)', title='Quantity'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=55, b=20)
    )
    return fig

def create_hazard_breakdown_donut(hazards: List[Dict]) -> go.Figure:
    """
    Renders donut distribution of identified hazards by severity.
    """
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for h in hazards:
        sev = h.get("severity", "Medium").title()
        if sev in counts:
            counts[sev] += 1
        else:
            counts["Medium"] += 1

    labels = [k for k, v in counts.items() if v > 0]
    values = [v for k, v in counts.items() if v > 0]
    
    color_map = {
        "Critical": "#EF4444",
        "High": "#F97316",
        "Medium": "#EAB308",
        "Low": "#10B981"
    }
    colors = [color_map.get(k, "#64748B") for k in labels]

    if not values:
        labels = ["Zero Hazards"]
        values = [1]
        colors = ["#10B981"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color='#0F172A', width=2)),
        textinfo='label+value',
        hoverinfo='label+percent'
    )])

    fig.update_layout(
        **DARK_LAYOUT,
        height=220,
        title={'text': "Hazard Severity Distribution", 'font': {'size': 14, 'color': '#94A3B8'}},
        showlegend=False,
        margin=dict(l=15, r=15, t=35, b=15)
    )
    return fig
