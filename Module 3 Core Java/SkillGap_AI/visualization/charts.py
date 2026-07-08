"""
SkillGap AI - Plotly Visualization Module
Generates all interactive charts and visualizations for the dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List, Dict, Any, Optional
import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# Color Palette
# ──────────────────────────────────────────────────────────────────────────────
COLORS = {
    "primary": "#667EEA",
    "secondary": "#764BA2",
    "success": "#00CC88",
    "warning": "#FFA500",
    "danger": "#FF6B6B",
    "info": "#00C9FF",
    "dark": "#1E1E2E",
    "card": "#2A2A3E",
    "text": "#E2E8F0",
}

GRADIENT_COLORS = [
    "#667EEA", "#764BA2", "#F093FB", "#F5576C",
    "#4FACFE", "#00F2FE", "#43E97B", "#38F9D7"
]

CHART_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E2E8F0", family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
)


def gauge_chart(
    value: float,
    title: str,
    max_val: float = 100,
    suffix: str = "%",
    color_thresholds: Optional[List] = None
) -> go.Figure:
    """
    Create an animated gauge/meter chart.
    
    Args:
        value: Current value to display
        title: Chart title
        max_val: Maximum scale value
        suffix: Value suffix (% or /100)
        color_thresholds: Custom color thresholds [[value, color], ...]
    
    Returns:
        Plotly Figure object
    """
    if color_thresholds is None:
        color_thresholds = [
            [0, COLORS["danger"]],
            [0.4, COLORS["warning"]],
            [0.6, COLORS["success"]],
            [0.8, COLORS["primary"]],
        ]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={"text": title, "font": {"size": 16, "color": COLORS["text"]}},
        number={"suffix": suffix, "font": {"size": 36, "color": COLORS["primary"]}},
        gauge={
            "axis": {
                "range": [0, max_val],
                "tickfont": {"color": COLORS["text"]},
                "tickwidth": 2,
            },
            "bar": {"color": COLORS["primary"], "thickness": 0.35},
            "bgcolor": COLORS["card"],
            "borderwidth": 2,
            "bordercolor": COLORS["primary"],
            "steps": [
                {"range": [0, max_val * 0.4], "color": "rgba(255,107,107,0.15)"},
                {"range": [max_val * 0.4, max_val * 0.7], "color": "rgba(255,165,0,0.15)"},
                {"range": [max_val * 0.7, max_val], "color": "rgba(0,204,136,0.15)"},
            ],
            "threshold": {
                "line": {"color": COLORS["secondary"], "width": 4},
                "thickness": 0.75,
                "value": value
            }
        }
    ))
    
    fig.update_layout(**CHART_THEME, height=280)
    return fig


def radar_chart(
    categories: List[str],
    values: List[float],
    title: str = "Skill Coverage Radar"
) -> go.Figure:
    """
    Create a radar/spider chart for skill coverage visualization.
    
    Args:
        categories: Skill category names
        values: Coverage percentages (0-100)
        title: Chart title
    
    Returns:
        Plotly Figure object
    """
    # Close the radar by repeating first value
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    # Filled area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(102,126,234,0.25)",
        line=dict(color=COLORS["primary"], width=2),
        name="Your Skills",
        hovertemplate="<b>%{theta}</b><br>Coverage: %{r:.1f}%<extra></extra>"
    ))
    
    # Ideal boundary
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories_closed),
        theta=categories_closed,
        line=dict(color=COLORS["secondary"], width=1, dash="dot"),
        name="Target (100%)",
        hoverinfo="skip"
    ))
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text=title, font=dict(size=14, color=COLORS["text"])),
        polar=dict(
            bgcolor=COLORS["card"],
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=COLORS["text"], size=9),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)"
            ),
            angularaxis=dict(
                tickfont=dict(color=COLORS["text"], size=10),
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)"
            )
        ),
        showlegend=True,
        legend=dict(font=dict(color=COLORS["text"])),
        height=380
    )
    return fig


def skill_bar_chart(
    skills: List[str],
    values: List[float],
    title: str = "Skill Distribution",
    horizontal: bool = True
) -> go.Figure:
    """
    Create a bar chart for skill scores or frequencies.
    
    Args:
        skills: Skill names
        values: Skill scores/counts
        title: Chart title
        horizontal: If True, creates horizontal bar chart
    
    Returns:
        Plotly Figure object
    """
    # Color gradient based on values
    max_val = max(values) if values else 1
    colors = [
        f"rgba({102 + int(153 * v/max_val)},{126 + int(74 * v/max_val)},{234 - int(100 * v/max_val)},0.85)"
        for v in values
    ]
    
    if horizontal:
        fig = go.Figure(go.Bar(
            y=skills,
            x=values,
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color=COLORS["primary"], width=0.5)
            ),
            hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>",
            text=[f"{v:.0f}" for v in values],
            textposition="outside",
            textfont=dict(color=COLORS["text"], size=10)
        ))
    else:
        fig = go.Figure(go.Bar(
            x=skills,
            y=values,
            marker=dict(
                color=colors,
                line=dict(color=COLORS["primary"], width=0.5)
            ),
            hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>",
        ))
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text=title, font=dict(size=14, color=COLORS["text"])),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color=COLORS["text"])),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color=COLORS["text"])),
        height=max(300, 30 * len(skills)) if horizontal else 350
    )
    return fig


def pie_chart(
    labels: List[str],
    values: List[float],
    title: str = "Distribution",
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Create a donut/pie chart.
    
    Args:
        labels: Category labels
        values: Corresponding values
        title: Chart title
        colors: Optional custom colors
    
    Returns:
        Plotly Figure object
    """
    if colors is None:
        colors = GRADIENT_COLORS[:len(labels)]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(
            colors=colors,
            line=dict(color=COLORS["dark"], width=2)
        ),
        textinfo="label+percent",
        textfont=dict(color=COLORS["text"], size=11),
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>%{percent}<extra></extra>"
    ))
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text=title, font=dict(size=14, color=COLORS["text"])),
        showlegend=True,
        legend=dict(font=dict(color=COLORS["text"]), bgcolor="rgba(0,0,0,0)"),
        height=320,
        annotations=[dict(
            text=f"{sum(values)}<br>Total",
            x=0.5, y=0.5,
            font=dict(size=14, color=COLORS["text"]),
            showarrow=False
        )]
    )
    return fig


def job_role_bar_chart(predictions: List[Dict]) -> go.Figure:
    """
    Create a horizontal bar chart for job role confidence scores.
    
    Args:
        predictions: List of {role, confidence} dicts
    
    Returns:
        Plotly Figure object
    """
    roles = [p["role"] for p in predictions]
    confidences = [p["confidence"] for p in predictions]
    
    # Color by rank
    bar_colors = [COLORS["primary"], COLORS["secondary"], "#4FACFE", "#00F2FE", "#43E97B"]
    
    fig = go.Figure(go.Bar(
        y=roles[::-1],
        x=confidences[::-1],
        orientation="h",
        marker=dict(
            color=bar_colors[:len(roles)][::-1],
            line=dict(color="rgba(255,255,255,0.2)", width=1)
        ),
        text=[f"{c:.1f}%" for c in confidences[::-1]],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=11),
        hovertemplate="<b>%{y}</b><br>Confidence: %{x:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="🤖 Job Role Predictions", font=dict(size=14, color=COLORS["text"])),
        xaxis=dict(
            range=[0, 110],
            title="Confidence Score (%)",
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color=COLORS["text"])
        ),
        yaxis=dict(tickfont=dict(color=COLORS["text"])),
        height=320
    )
    return fig


def ats_breakdown_chart(category_scores: Dict, weights: Dict) -> go.Figure:
    """
    Create a combined chart showing ATS score breakdown.
    
    Args:
        category_scores: {category: score (0-100)} dict
        weights: {category: weight} dict
    
    Returns:
        Plotly Figure object
    """
    categories = list(category_scores.keys())
    scores = list(category_scores.values())
    weights_list = [weights.get(c, 0) for c in categories]
    
    # Weighted actual scores
    weighted = [s * w / 100 for s, w in zip(scores, weights_list)]
    
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])
    
    # Bar chart: raw scores per category
    fig.add_trace(
        go.Bar(
            x=categories,
            y=scores,
            name="Category Score",
            marker=dict(color=GRADIENT_COLORS[:len(categories)]),
            hovertemplate="<b>%{x}</b><br>Score: %{y}/100<extra></extra>"
        ),
        row=1, col=1
    )
    
    # Pie chart: weight distribution
    fig.add_trace(
        go.Pie(
            labels=categories,
            values=weights_list,
            name="Weight",
            hole=0.4,
            marker=dict(colors=GRADIENT_COLORS[:len(categories)]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Weight: %{value}%<extra></extra>"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="📊 ATS Score Breakdown", font=dict(size=14, color=COLORS["text"])),
        showlegend=False,
        height=350
    )
    fig.update_xaxes(tickfont=dict(color=COLORS["text"]), gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(tickfont=dict(color=COLORS["text"]), gridcolor="rgba(255,255,255,0.1)")
    
    return fig


def skills_comparison_chart(
    matching_skills: List[str],
    missing_skills: List[str]
) -> go.Figure:
    """
    Create a chart comparing matching vs missing skills.
    
    Args:
        matching_skills: Skills found in both resume and JD
        missing_skills: Skills in JD but not in resume
    
    Returns:
        Plotly Figure object
    """
    labels = ["✅ Matching Skills", "❌ Missing Skills"]
    values = [len(matching_skills), len(missing_skills)]
    colors = [COLORS["success"], COLORS["danger"]]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors, line=dict(color=COLORS["dark"], width=3)),
        textinfo="label+value+percent",
        textfont=dict(color=COLORS["text"], size=12),
        pull=[0.05, 0],
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
    ))
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="🔍 Skill Match Distribution", font=dict(size=14, color=COLORS["text"])),
        legend=dict(font=dict(color=COLORS["text"])),
        height=300,
        annotations=[dict(
            text=f"{len(matching_skills)+len(missing_skills)}<br>Total",
            x=0.5, y=0.5,
            font=dict(size=14, color=COLORS["text"]),
            showarrow=False
        )]
    )
    return fig


def learning_progress_chart(roadmap: List[str], completed: int = 0) -> go.Figure:
    """
    Create a visual learning progress timeline.
    
    Args:
        roadmap: List of learning steps
        completed: Number of completed steps
    
    Returns:
        Plotly Figure object
    """
    steps = roadmap[:8]
    n = len(steps)
    
    y_vals = list(range(n, 0, -1))
    colors_list = [
        COLORS["success"] if i < completed else COLORS["primary"]
        for i in range(n)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[1] * n,
        y=y_vals,
        orientation="v",
        marker=dict(color=colors_list, line=dict(width=0)),
        width=0.5,
        showlegend=False,
        hoverinfo="skip"
    ))
    
    # Text annotations
    for i, (step, y) in enumerate(zip(steps, y_vals)):
        status = "✅" if i < completed else "📌"
        fig.add_annotation(
            x=0.5,
            y=y,
            text=f"{status} {step[:50]}{'...' if len(step) > 50 else ''}",
            showarrow=False,
            font=dict(size=11, color=COLORS["text"]),
            align="left",
            xanchor="center"
        )
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="🗺️ Learning Roadmap", font=dict(size=14, color=COLORS["text"])),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=max(300, 45 * n)
    )
    return fig


def match_percentage_timeline(history: List[Dict]) -> go.Figure:
    """
    Show match percentage over multiple resume analyses (if session history exists).
    
    Args:
        history: List of {timestamp, match_pct, ats_score} dicts
    
    Returns:
        Plotly Figure object
    """
    if not history:
        return go.Figure()
    
    df = pd.DataFrame(history)
    
    fig = go.Figure()
    
    if "match_pct" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.get("timestamp", list(range(len(df)))),
            y=df["match_pct"],
            name="Skill Match %",
            mode="lines+markers",
            line=dict(color=COLORS["primary"], width=3),
            marker=dict(size=8, color=COLORS["primary"]),
        ))
    
    if "ats_score" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.get("timestamp", list(range(len(df)))),
            y=df["ats_score"],
            name="ATS Score",
            mode="lines+markers",
            line=dict(color=COLORS["success"], width=3),
            marker=dict(size=8, color=COLORS["success"]),
        ))
    
    fig.update_layout(
        **CHART_THEME,
        title=dict(text="📈 Progress Over Time", font=dict(size=14, color=COLORS["text"])),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color=COLORS["text"])),
        yaxis=dict(range=[0, 105], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color=COLORS["text"])),
        legend=dict(font=dict(color=COLORS["text"])),
        height=300
    )
    return fig
