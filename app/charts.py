"""Interactive Plotly Visualizations for Stock Intelligence."""

import plotly.graph_objects as go


def create_perspective_gauge(view_str: str, confidence: float) -> go.Figure:
    """
    Creates a sleek dark-themed radial speedometer gauge for the AI Investment Perspective.
    
    Args:
        view_str: "bullish", "cautiously_bullish", "neutral", "cautiously_bearish", or "bearish"
        confidence: Float from 0.0 to 1.0 representing model confidence
    """
    view_normalized = view_str.lower().strip()
    
    # Map overall view string to score scale (0 to 100)
    score_mapping = {
        "bearish": 12,
        "cautiously_bearish": 32,
        "neutral": 50,
        "cautiously_bullish": 68,
        "bullish": 88,
    }
    base_score = score_mapping.get(view_normalized, 50)
    
    # Adjust slightly with confidence
    if "bullish" in view_normalized:
        final_score = min(98, base_score + (confidence * 8))
        needle_color = "#10B981"
    elif "bearish" in view_normalized:
        final_score = max(5, base_score - (confidence * 8))
        needle_color = "#F43F5E"
    else:
        final_score = base_score
        needle_color = "#F59E0B"

    display_title = view_str.replace("_", " ").upper()
    
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=final_score,
            number={
                "suffix": "%",
                "font": {"size": 26, "color": "#F8FAFC", "family": "JetBrains Mono"},
                "valueformat": ".0f",
            },
            title={
                "text": f"<span style='font-size:1.15em;font-weight:700;color:{needle_color};font-family:Outfit;'>{display_title}</span><br><span style='font-size:0.75em;color:#94A3B8;font-family:Plus Jakarta Sans;'>AI Confidence: {confidence:.0%}</span>",
                "font": {"size": 18, "family": "Outfit"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#475569",
                    "tickvals": [10, 30, 50, 70, 90],
                    "ticktext": ["BEAR", "C-BEAR", "NEUTRAL", "C-BULL", "BULL"],
                    "tickfont": {"size": 10, "color": "#94A3B8", "family": "Outfit"},
                },
                "bar": {"color": needle_color, "thickness": 0.28},
                "bgcolor": "rgba(15, 23, 42, 0.4)",
                "borderwidth": 1,
                "bordercolor": "rgba(255, 255, 255, 0.08)",
                "steps": [
                    {"range": [0, 20], "color": "rgba(244, 63, 94, 0.22)"},
                    {"range": [20, 40], "color": "rgba(251, 146, 60, 0.20)"},
                    {"range": [40, 60], "color": "rgba(245, 158, 11, 0.20)"},
                    {"range": [60, 80], "color": "rgba(52, 211, 153, 0.20)"},
                    {"range": [80, 100], "color": "rgba(16, 185, 129, 0.25)"},
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Plus Jakarta Sans", "color": "#F8FAFC"},
        margin=dict(l=25, r=25, t=50, b=15),
        height=240,
    )
    return fig


def create_factors_breakdown_chart(positive_count: int, negative_count: int, uncertainty_count: int) -> go.Figure:
    """
    Creates an interactive horizontal sentiment/factor balance bar.
    """
    labels = ["Positive Catalysts", "Negative Risks", "Uncertainties"]
    values = [positive_count, negative_count, uncertainty_count]
    colors = ["#10B981", "#F43F5E", "#F59E0B"]

    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(255,255,255,0.15)", width=1),
                ),
                text=values,
                textposition="auto",
                textfont=dict(color="#FFFFFF", family="JetBrains Mono", size=13),
            )
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Plus Jakarta Sans", "color": "#94A3B8"},
        margin=dict(l=10, r=20, t=10, b=10),
        height=140,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            showticklabels=True,
        ),
        yaxis=dict(
            autorange="reversed",
            showgrid=False,
            tickfont=dict(size=12, color="#E2E8F0"),
        ),
    )
    return fig


def create_fundamentals_card_chart(financials) -> go.Figure | None:
    """
    Creates a clean dark mini bar chart showing available fundamental ratios.
    """
    metrics = []
    values = []
    
    if financials.pe_ratio is not None:
        metrics.append("P/E Ratio")
        values.append(financials.pe_ratio)
    if financials.pb_ratio is not None:
        metrics.append("P/B Ratio")
        values.append(financials.pb_ratio)
    if financials.net_margin is not None:
        metrics.append("Net Margin %")
        values.append(financials.net_margin * 100 if financials.net_margin < 1 else financials.net_margin)
    if financials.operating_margin is not None:
        metrics.append("Op. Margin %")
        values.append(financials.operating_margin * 100 if financials.operating_margin < 1 else financials.operating_margin)
    if financials.debt_to_equity is not None:
        metrics.append("Debt/Equity")
        values.append(financials.debt_to_equity)

    if not metrics:
        return None

    fig = go.Figure(
        data=[
            go.Bar(
                x=metrics,
                y=values,
                marker=dict(
                    color="#38BDF8",
                    line=dict(color="rgba(56, 189, 248, 0.4)", width=1),
                ),
                text=[f"{v:.1f}" for v in values],
                textposition="outside",
                textfont=dict(color="#F8FAFC", family="JetBrains Mono", size=11),
            )
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Plus Jakarta Sans", "color": "#94A3B8"},
        margin=dict(l=20, r=20, t=25, b=25),
        height=190,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color="#CBD5E1"),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            showticklabels=False,
        ),
    )
    return fig
