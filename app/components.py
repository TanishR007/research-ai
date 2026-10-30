"""Reusable UI components for Stock Intelligence Streamlit Application."""

import textwrap
from urllib.parse import urlparse
from models.company import CompanyIdentity
from models.market import MarketData
from models.financials import FinancialData
from models.movement import MovementAnalysis
from models.report import StockPerspective
from models.evidence import Claim
from models.analysis import NewsEvent


def render_hero_header(company: CompanyIdentity, market: MarketData | None) -> str:
    """Renders high-impact company hero banner with ticker and exchange badges."""
    price_badge = ""
    if market:
        is_positive = (market.percent_change or 0) >= 0
        change_sign = "+" if is_positive else ""
        badge_cls = "badge-bullish" if is_positive else "badge-bearish"
        arrow = "▲" if is_positive else "▼"
        pct = market.percent_change or 0
        price_badge = f"""<div class="badge {badge_cls}"><span>{arrow}</span><span>{change_sign}{pct:.2f}%</span></div>"""

    html = f"""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.4rem; flex-wrap: wrap;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                    {company.ticker}
                </span>
                <span class="badge badge-cyan">{company.exchange}</span>
                <span class="badge" style="background: rgba(255,255,255,0.08); color: #CBD5E1;">{company.country}</span>
                {price_badge}
            </div>
            <div style="font-size: 1.15rem; font-weight: 500; color: #94A3B8;">
                {company.company_name}
            </div>
        </div>
    </div>
</div>
"""
    return textwrap.dedent(html).strip()


def render_metric_cards(market: MarketData | None, financials: FinancialData | None) -> str:
    """Renders custom glassmorphic KPI cards for price, volume, and fundamentals."""
    cards_html = []

    # Card 1: Live Price
    if market and market.price is not None:
        is_positive = (market.percent_change or 0) >= 0
        chg_sign = "+" if is_positive else ""
        chg_val = market.change or 0
        chg_pct = market.percent_change or 0
        color = "#10B981" if is_positive else "#F43F5E"
        curr = market.currency or "$"

        cards_html.append(f"""
<div class="metric-card">
    <div class="metric-label">Market Price</div>
    <div class="metric-value">{curr}{market.price:,.2f}</div>
    <div style="font-size: 0.85rem; color: {color}; margin-top: 0.35rem; font-family: 'JetBrains Mono';">
        {chg_sign}{chg_val:.2f} ({chg_sign}{chg_pct:.2f}%)
    </div>
</div>
""")

    # Card 2: Volume
    if market and market.volume is not None:
        cards_html.append(f"""
<div class="metric-card">
    <div class="metric-label">Trading Volume</div>
    <div class="metric-value">{market.volume:,}</div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 0.35rem;">
        Shares traded
    </div>
</div>
""")

    # Card 3: P/E & P/B Ratios
    if financials:
        pe_str = f"{financials.pe_ratio:.1f}x" if financials.pe_ratio else "N/A"
        pb_str = f"{financials.pb_ratio:.1f}x" if financials.pb_ratio else "N/A"
        cards_html.append(f"""
<div class="metric-card">
    <div class="metric-label">Valuation (P/E · P/B)</div>
    <div class="metric-value" style="font-size: 1.45rem;">
        {pe_str} <span style="font-size: 0.9rem; color: #64748B;">/</span> {pb_str}
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 0.35rem;">
        TTM Ratios
    </div>
</div>
""")

    # Card 4: Operating & Net Margin
    if financials and (financials.net_margin is not None or financials.operating_margin is not None):
        nm = f"{financials.net_margin * 100:.1f}%" if financials.net_margin else "N/A"
        om = f"{financials.operating_margin * 100:.1f}%" if financials.operating_margin else "N/A"
        cards_html.append(f"""
<div class="metric-card">
    <div class="metric-label">Margins (Net · Op)</div>
    <div class="metric-value" style="font-size: 1.45rem;">
        {nm} <span style="font-size: 0.9rem; color: #64748B;">/</span> {om}
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 0.35rem;">
        Profitability
    </div>
</div>
""")

    body = "".join([textwrap.dedent(c).strip() for c in cards_html])
    return f'<div class="metric-grid">{body}</div>'


def render_movement_analysis(movement: MovementAnalysis) -> str:
    """Renders prominent callout box specifically explaining stock movement."""
    contributing_html = "".join([f"<li style='margin-bottom: 0.4rem;'>{factor}</li>" for factor in movement.contributing_factors])
    evidence_html = "".join([f"<li style='margin-bottom: 0.4rem;'>{ev}</li>" for ev in movement.supporting_evidence])
    uncertainties_html = "".join([f"<li style='margin-bottom: 0.4rem;'>{unc}</li>" for unc in movement.uncertainties])
    
    sources_html = []
    for s in movement.sources:
        try:
            domain = urlparse(s).netloc or s
        except Exception:
            domain = s
        sources_html.append(f'<a href="{s}" target="_blank" class="source-chip">🔗 {domain}</a>')

    html = f"""
<div class="movement-box">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
        <span class="pulse-dot" style="background: #38BDF8;"></span>
        <span style="font-family: 'Outfit'; font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">
            Market Movement Analysis
        </span>
    </div>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #E2E8F0; margin-bottom: 1rem;">
        {movement.answer}
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem;">
        {f'''<div style="background: rgba(15, 23, 42, 0.6); padding: 1rem; border-radius: 10px;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #38BDF8; text-transform: uppercase; margin-bottom: 0.5rem;">Contributing Factors</div>
            <ul style="padding-left: 1.2rem; font-size: 0.92rem; color: #CBD5E1; margin: 0;">{contributing_html}</ul>
        </div>''' if contributing_html else ''}
        {f'''<div style="background: rgba(15, 23, 42, 0.6); padding: 1rem; border-radius: 10px;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #10B981; text-transform: uppercase; margin-bottom: 0.5rem;">Supporting Evidence</div>
            <ul style="padding-left: 1.2rem; font-size: 0.92rem; color: #CBD5E1; margin: 0;">{evidence_html}</ul>
        </div>''' if evidence_html else ''}
    </div>
    {f'''<div style="margin-top: 1rem; padding: 0.75rem 1rem; background: rgba(245, 158, 11, 0.08); border-left: 3px solid #F59E0B; border-radius: 0 8px 8px 0;">
        <div style="font-size: 0.85rem; font-weight: 600; color: #F59E0B; text-transform: uppercase; margin-bottom: 0.35rem;">Key Uncertainties</div>
        <ul style="padding-left: 1.2rem; font-size: 0.9rem; color: #E2E8F0; margin: 0;">{uncertainties_html}</ul>
    </div>''' if uncertainties_html else ''}
    {f'''<div style="margin-top: 1rem; display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem;">
        <span style="font-size: 0.78rem; color: #64748B; margin-right: 0.5rem;">Sources:</span>
        {"".join(sources_html)}
    </div>''' if sources_html else ''}
</div>
"""
    return textwrap.dedent(html).strip()


def render_perspective_reasoning(perspective: StockPerspective) -> str:
    """Renders the AI Investment reasoning and catalysts."""
    catalysts_html = "".join([f"<li style='margin-bottom: 0.4rem;'>{cat}</li>" for cat in perspective.catalysts_to_watch])
    risks_html = "".join([f"<li style='margin-bottom: 0.4rem;'>{r}</li>" for r in perspective.key_risks])

    html = f"""
<div class="glass-panel">
    <h4 style="margin-top: 0; margin-bottom: 0.75rem; color: #F8FAFC;">Analyst Synthesis & Reasoning</h4>
    <p style="font-size: 0.98rem; line-height: 1.65; color: #CBD5E1; margin-bottom: 1.25rem;">
        {perspective.reasoning}
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
        {f'''<div style="background: rgba(15, 23, 42, 0.5); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 0.85rem; font-weight: 600; color: #F43F5E; text-transform: uppercase; margin-bottom: 0.5rem;">⚠️ Key Risks</div>
            <ul style="padding-left: 1.2rem; font-size: 0.9rem; color: #CBD5E1; margin: 0;">{risks_html}</ul>
        </div>''' if risks_html else ''}
        {f'''<div style="background: rgba(15, 23, 42, 0.5); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 0.85rem; font-weight: 600; color: #38BDF8; text-transform: uppercase; margin-bottom: 0.5rem;">🔭 Catalysts to Watch</div>
            <ul style="padding-left: 1.2rem; font-size: 0.9rem; color: #CBD5E1; margin: 0;">{catalysts_html}</ul>
        </div>''' if catalysts_html else ''}
    </div>
</div>
"""
    return textwrap.dedent(html).strip()


def render_factor_cards(positive_factors: list[str], negative_factors: list[str], uncertainties: list[str]) -> str:
    """Renders visual cards comparing positive vs negative drivers."""
    pos_html = []
    for f in positive_factors:
        pos_html.append(f"""
<div class="factor-card factor-positive">
    <span style="color: #10B981; font-weight: 600; margin-right: 0.4rem;">+</span>
    <span style="font-size: 0.92rem; color: #E2E8F0;">{f}</span>
</div>
""")
        
    neg_html = []
    if negative_factors:
        for f in negative_factors:
            neg_html.append(f"""
<div class="factor-card factor-negative">
    <span style="color: #F43F5E; font-weight: 600; margin-right: 0.4rem;">-</span>
    <span style="font-size: 0.92rem; color: #E2E8F0;">{f}</span>
</div>
""")
    else:
        neg_html.append('<div style="color: #64748B; font-size: 0.9rem; padding: 0.75rem;">No clearly supported negative factors identified.</div>')

    unc_html = []
    for u in uncertainties:
        unc_html.append(f"""
<div class="factor-card factor-uncertain">
    <span style="color: #F59E0B; font-weight: 600; margin-right: 0.4rem;">?</span>
    <span style="font-size: 0.92rem; color: #E2E8F0;">{u}</span>
</div>
""")

    pos_body = "".join([textwrap.dedent(p).strip() for p in pos_html])
    neg_body = "".join([textwrap.dedent(n).strip() for n in neg_html])
    unc_body = "".join([textwrap.dedent(u).strip() for u in unc_html])

    html = f"""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.25rem;">
    <div class="glass-panel">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #10B981;">Positive Catalysts</h4>
            <span class="badge badge-bullish">{len(positive_factors)}</span>
        </div>
        {pos_body}
    </div>
    <div class="glass-panel">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #F43F5E;">Negative Factors</h4>
            <span class="badge badge-bearish">{len(negative_factors)}</span>
        </div>
        {neg_body}
    </div>
</div>
{f'''<div class="glass-panel" style="margin-top: 1rem;">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <h4 style="margin: 0; color: #F59E0B;">Uncertainties & Open Questions</h4>
        <span class="badge badge-neutral">{len(uncertainties)}</span>
    </div>
    {unc_body}
</div>''' if unc_body else ''}
"""
    return textwrap.dedent(html).strip()


def render_claims_list(claims: list[Claim]) -> str:
    """Renders structured verifiable claim cards with category badges and sources."""
    if not claims:
        return "<p style='color: #64748B;'>No structured claims extracted.</p>"

    type_styles = {
        "market": ("badge-cyan", "MARKET"),
        "fundamental": ("badge-neutral", "FUNDAMENTAL"),
        "news": ("badge-purple", "NEWS"),
        "analyst": ("badge-bullish", "ANALYST"),
    }

    cards_html = []
    for claim in claims:
        category_val = claim.claim_type.value.lower() if hasattr(claim.claim_type, "value") else str(claim.claim_type).lower()
        badge_cls, label = type_styles.get(category_val, ("badge-cyan", category_val.upper()))
        
        sources_html = []
        for s in claim.source_urls:
            try:
                domain = urlparse(s).netloc or s
            except Exception:
                domain = s
            sources_html.append(f'<a href="{s}" target="_blank" class="source-chip">🔗 {domain}</a>')

        card = f"""
<div class="claim-card">
    <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; margin-bottom: 0.5rem;">
        <span class="badge {badge_cls}">{label}</span>
    </div>
    <p style="margin: 0.4rem 0 0.6rem 0; font-size: 0.95rem; line-height: 1.5; color: #F1F5F9;">
        {claim.statement}
    </p>
    {f'<div style="display: flex; flex-wrap: wrap; gap: 0.35rem;">{"".join(sources_html)}</div>' if sources_html else ''}
</div>
"""
        cards_html.append(textwrap.dedent(card).strip())

    return "".join(cards_html)


def render_news_events_timeline(events: list[NewsEvent]) -> str:
    """Renders structured news events with date and source links."""
    if not events:
        return "<p style='color: #64748B;'>No concrete news events extracted.</p>"

    events_html = []
    for ev in events:
        date_str = ev.published_at.strftime("%b %d, %Y") if ev.published_at else "Recent"
        try:
            domain = urlparse(ev.source_url).netloc or ev.source_url
        except Exception:
            domain = ev.source_url

        card = f"""
<div class="claim-card">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
        <span style="font-family: 'Outfit'; font-weight: 600; color: #F8FAFC; font-size: 1rem;">
            {ev.title}
        </span>
        <span style="font-size: 0.78rem; color: #64748B;">{date_str}</span>
    </div>
    <p style="font-size: 0.9rem; color: #94A3B8; margin: 0.3rem 0 0.6rem 0; line-height: 1.5;">
        {ev.description}
    </p>
    <a href="{ev.source_url}" target="_blank" class="source-chip">
        🔗 {domain}
    </a>
</div>
"""
        events_html.append(textwrap.dedent(card).strip())

    return "".join(events_html)
