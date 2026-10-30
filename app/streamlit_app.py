import sys
from pathlib import Path
import textwrap
import time
import streamlit as st

# Setup python paths for workspace modules
root_path = Path(__file__).resolve().parents[1]
sys.path.extend([str(root_path), str(root_path / "src")])

from services.research import run_research
from config.settings import settings
from app.styles import GLOBAL_CSS
from app.mock_data import get_mock_research_state
from app.charts import (
    create_perspective_gauge,
    create_factors_breakdown_chart,
    create_fundamentals_card_chart,
)
from app.components import (
    render_hero_header,
    render_metric_cards,
    render_movement_analysis,
    render_perspective_reasoning,
    render_factor_cards,
    render_claims_list,
    render_news_events_timeline,
)

# Helper function to prevent markdown from parsing indented HTML as <pre><code> blocks
def md_html(html_str: str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)


# 1. Page Configuration
st.set_page_config(
    page_title="Stock Intelligence Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Inject Global Design System CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

keys_configured = bool(
    settings.gemini_api_key
    and settings.tavily_api_key
    and settings.twelve_data_api_key
    and settings.finnhub_api_key
)

# 3. Header & Branding with Mode Toggle
header_col, mode_col = st.columns([7, 3])
with header_col:
    md_html(
        """
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
                <span style="font-size: 1.6rem;">⚡</span>
                <span style="font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; color: #F8FAFC;">
                    STOCK INTELLIGENCE <span style="background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">TERMINAL</span>
                </span>
                <span class="badge badge-cyan" style="font-size: 0.72rem; padding: 0.15rem 0.5rem; margin-left: 0.5rem;">v2.0 MULTI-AGENT</span>
            </div>
            <div style="font-size: 0.92rem; color: #94A3B8;">
                Institutional-grade financial intelligence engine powered by LangGraph, Gemini, TwelveData & Tavily
            </div>
        </div>
        """
    )

with mode_col:
    demo_mode = st.toggle(
        "⚡ Demo Simulation Mode",
        value=not keys_configured,
        help="Run high-fidelity simulated multi-agent research without requiring API keys.",
    )
    if demo_mode:
        st.caption("<span style='color: #38BDF8;'>● Demo Mode Active (No API keys required)</span>", unsafe_allow_html=True)
    else:
        st.caption("<span style='color: #10B981;'>● Live API Mode Active</span>", unsafe_allow_html=True)

# 4. Search State Management & Quick Prompts
if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

def set_quick_query(text: str):
    st.session_state["query_input"] = text

# Quick Prompt Pill Chips
md_html("<div style='font-size: 0.8rem; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 0.4rem;'>Quick Research Prompts:</div>")

chip_cols = st.columns([1.6, 1.6, 1.8, 1.2, 1.2])
with chip_cols[0]:
    if st.button("🔥 NVDA: Why did it drop?", key="q1", use_container_width=True):
        set_quick_query("Why did NVDA fall today?")
with chip_cols[1]:
    if st.button("🍎 AAPL: Developments", key="q2", use_container_width=True):
        set_quick_query("AAPL latest news and research")
with chip_cols[2]:
    if st.button("⚡ TSLA: Valuation & Margins", key="q3", use_container_width=True):
        set_quick_query("TSLA fundamental valuation check")
with chip_cols[3]:
    if st.button("💻 MSFT", key="q4", use_container_width=True):
        set_quick_query("Microsoft MSFT")
with chip_cols[4]:
    if st.button("📦 AMZN", key="q5", use_container_width=True):
        set_quick_query("Amazon AMZN")

# Main Search Input
search_col, btn_col = st.columns([5, 1])

with search_col:
    query = st.text_input(
        "Research a stock or query",
        value=st.session_state["query_input"],
        placeholder="Enter a ticker or question (e.g. 'AAPL', 'Why did NVDA fall today?', 'Tesla margins')",
        label_visibility="collapsed",
    )

with btn_col:
    execute_search = st.button("Analyze ⚡", type="primary", use_container_width=True)

# 5. Search Execution
if execute_search:
    if not query.strip():
        st.warning("Please enter a stock ticker or research question.")
        st.stop()

    st.session_state["last_executed_query"] = query

    if demo_mode:
        # Multi-Agent Execution Stepper (Demo Simulation)
        with st.status("⚡ Orchestrating Multi-Agent Pipeline (Demo Simulation)...", expanded=True) as status_box:
            st.write("🔍 **Ticker Resolver:** Identifying securities symbol, exchange, and country...")
            time.sleep(0.4)
            st.write("📡 **Data Ingestion:** Fetching live quotes (TwelveData), fundamentals (Finnhub), and news (Tavily)...")
            time.sleep(0.5)
            st.write("🧠 **Impact Analysis:** Distilling factual events and cross-referencing market movement...")
            time.sleep(0.4)
            st.write("📑 **Synthesizer & Perspective:** Compiling institutional report and AI perspective...")
            time.sleep(0.4)

            result = get_mock_research_state(query)
            status_box.update(label="✅ Research Complete (Demo Simulation)", state="complete", expanded=False)
            st.session_state["latest_result"] = result
    else:
        # Multi-Agent Execution Stepper (Live API Mode)
        with st.status("⚡ Orchestrating Multi-Agent Pipeline...", expanded=True) as status_box:
            st.write("🔍 **Ticker Resolver:** Identifying securities symbol, exchange, and country...")
            st.write("📡 **Data Ingestion:** Fetching live quotes (TwelveData), fundamentals (Finnhub), and news (Tavily)...")
            st.write("🧠 **Impact Analysis:** Distilling factual events and cross-referencing market movement...")
            st.write("📑 **Synthesizer & Perspective:** Compiling institutional report and AI perspective...")

            try:
                result = run_research(query)
                status_box.update(label="✅ Research Complete", state="complete", expanded=False)
                st.session_state["latest_result"] = result
            except Exception as e:
                status_box.update(label="❌ Pipeline Execution Failed", state="error", expanded=True)
                st.error(f"Research failed: {e}")
                st.info("💡 **Tip:** Ensure your API keys (`GEMINI_API_KEY`, `TAVILY_API_KEY`, `TWELVE_DATA_API_KEY`, `FINNHUB_API_KEY`) are configured in `.env`.")
                st.stop()

# 6. Render Latest Results
if "latest_result" in st.session_state:
    result = st.session_state["latest_result"]
    company = result.company

    if company is None:
        st.error("Could not resolve company for the given query. Please verify the symbol or company name.")
        st.stop()

    # Step A: High-Impact Hero Banner
    md_html(render_hero_header(company, result.market_data))

    # Step B: Custom Metric Cards
    md_html(render_metric_cards(result.market_data, result.financial_data))

    # Step C: Movement Analysis (Highlight prominently if query asked about price movement)
    if result.movement_analysis:
        md_html(render_movement_analysis(result.movement_analysis))

    # Step D: Interactive Multi-Tab Deep Dive
    tab_perspective, tab_factors, tab_claims, tab_report = st.tabs([
        "🎯 AI Perspective & Catalysts",
        "📊 Factor Matrix & Fundamentals",
        "🔍 Verified Claims & News Events",
        "📑 Institutional Report",
    ])

    # TAB 1: AI Perspective & Catalysts
    with tab_perspective:
        if result.perspective:
            persp = result.perspective
            col_gauge, col_reasoning = st.columns([5, 7])

            with col_gauge:
                md_html("<div class='glass-panel'>")
                # Plotly Gauge Chart
                fig_gauge = create_perspective_gauge(persp.overall_view.value, persp.confidence)
                st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

                # Factor Breakdown Bar
                pos_count = len(persp.positive_factors)
                neg_count = len(persp.negative_factors)
                unc_count = len(persp.key_uncertainties)
                fig_breakdown = create_factors_breakdown_chart(pos_count, neg_count, unc_count)
                st.plotly_chart(fig_breakdown, use_container_width=True, config={"displayModeBar": False})
                md_html("</div>")

            with col_reasoning:
                md_html(render_perspective_reasoning(persp))
        else:
            st.info("Perspective assessment unavailable for this run.")

    # TAB 2: Factor Matrix & Fundamentals
    with tab_factors:
        col_factors, col_fund_chart = st.columns([7, 5])

        with col_factors:
            if result.analysis:
                pos = result.analysis.positive_factors
                neg = result.analysis.negative_factors
                unc = result.analysis.uncertainties
            elif result.perspective:
                pos = result.perspective.positive_factors
                neg = result.perspective.negative_factors
                unc = result.perspective.key_uncertainties
            else:
                pos, neg, unc = [], [], []

            md_html(render_factor_cards(pos, neg, unc))

        with col_fund_chart:
            md_html("<div class='glass-panel'>")
            md_html("<h4 style='margin-top: 0; color: #F8FAFC;'>Key Financial Metrics</h4>")
            if result.financial_data:
                fig_fund = create_fundamentals_card_chart(result.financial_data)
                if fig_fund:
                    st.plotly_chart(fig_fund, use_container_width=True, config={"displayModeBar": False})
                else:
                    st.write("Numerical ratios not populated for this asset.")

                # Summary details
                fin = result.financial_data
                md_html(
                    f"""
                    <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.6; margin-top: 0.75rem;">
                        <div>• <strong>P/E Ratio (TTM):</strong> {f'{fin.pe_ratio:.2f}' if fin.pe_ratio else 'N/A'}</div>
                        <div>• <strong>P/B Ratio:</strong> {f'{fin.pb_ratio:.2f}' if fin.pb_ratio else 'N/A'}</div>
                        <div>• <strong>Net Margin:</strong> {f'{fin.net_margin * 100:.1f}%' if fin.net_margin else 'N/A'}</div>
                        <div>• <strong>Operating Margin:</strong> {f'{fin.operating_margin * 100:.1f}%' if fin.operating_margin else 'N/A'}</div>
                        <div>• <strong>Debt/Equity:</strong> {f'{fin.debt_to_equity:.2f}' if fin.debt_to_equity else 'N/A'}</div>
                        <div>• <strong>Period Reported:</strong> {fin.latest_period or 'Latest'}</div>
                    </div>
                    """
                )
            else:
                st.write("Fundamental data currently unavailable.")
            md_html("</div>")

    # TAB 3: Verified Claims & News Events
    with tab_claims:
        col_claims, col_news = st.columns([1, 1])

        with col_claims:
            md_html(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; color: #38BDF8;">Verifiable Factual Claims</h4>
                    <span style="font-size: 0.8rem; color: #64748B;">Grounding & Auditability</span>
                </div>
                """
            )
            md_html(render_claims_list(result.claims))

        with col_news:
            md_html(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                    <h4 style="margin: 0; color: #A855F7;">Extracted News Events</h4>
                    <span style="font-size: 0.8rem; color: #64748B;">Concrete Reported Developments</span>
                </div>
                """
            )
            md_html(render_news_events_timeline(result.news_events))

    # TAB 4: Institutional Report
    with tab_report:
        if result.report:
            rep = result.report
            md_html(
                f"""
                <div class="glass-panel">
                    <h3 style="margin-top: 0; color: #38BDF8;">Executive Summary</h3>
                    <p style="font-size: 1.05rem; line-height: 1.7; color: #E2E8F0;">
                        {rep.executive_summary}
                    </p>
                    
                    <h4 style="color: #F8FAFC; margin-top: 1.5rem;">Market Snapshot</h4>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #94A3B8;">
                        {rep.market_snapshot}
                    </p>
                    
                    <h4 style="color: #F8FAFC; margin-top: 1.5rem;">Recent Developments</h4>
                    <ul style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.6;">
                        {"".join([f"<li>{dev}</li>" for dev in rep.recent_developments])}
                    </ul>
                </div>
                """
            )
        else:
            st.info("Comprehensive report synthesis unavailable.")
else:
    # Empty State: Modern Bento Showcase Grid
    md_html(
        """
        <div style="margin-top: 2rem;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.25rem;">
                <div class="glass-panel" style="padding: 1.75rem;">
                    <div style="font-size: 1.75rem; margin-bottom: 0.6rem;">⚡</div>
                    <div style="font-family: 'Outfit'; font-size: 1.2rem; font-weight: 700; color: #38BDF8; margin-bottom: 0.5rem;">
                        Multi-Agent Intelligence
                    </div>
                    <p style="font-size: 0.92rem; color: #94A3B8; line-height: 1.6; margin: 0;">
                        Orchestrates a specialized swarm of agents via <strong>LangGraph</strong>: symbol resolution, real-time TwelveData market quotes, Finnhub fundamentals, and Tavily web news.
                    </p>
                </div>
                <div class="glass-panel" style="padding: 1.75rem;">
                    <div style="font-size: 1.75rem; margin-bottom: 0.6rem;">🛡️</div>
                    <div style="font-family: 'Outfit'; font-size: 1.2rem; font-weight: 700; color: #10B981; margin-bottom: 0.5rem;">
                        Grounded & Auditable
                    </div>
                    <p style="font-size: 0.92rem; color: #94A3B8; line-height: 1.6; margin: 0;">
                        Built with strict anti-hallucination guardrails. Separates raw facts from analyst speculation, maps verifiable claims, and links directly to primary sources.
                    </p>
                </div>
                <div class="glass-panel" style="padding: 1.75rem;">
                    <div style="font-size: 1.75rem; margin-bottom: 0.6rem;">🎯</div>
                    <div style="font-family: 'Outfit'; font-size: 1.2rem; font-weight: 700; color: #A855F7; margin-bottom: 0.5rem;">
                        Movement & Sentiment Dial
                    </div>
                    <p style="font-size: 0.92rem; color: #94A3B8; line-height: 1.6; margin: 0;">
                        Ask natural questions like <em>"Why did NVDA drop today?"</em> to receive factor breakdowns, uncertainty flags, and an interactive confidence speedometer.
                    </p>
                </div>
            </div>
        </div>
        """
    )

    with st.expander("⚙️ API Configuration Guide"):
        st.markdown(
            """
            To run live research queries, configure your API keys in a `.env` file at the root of the project:
            ```env
            GEMINI_API_KEY=your_google_gemini_api_key
            TAVILY_API_KEY=your_tavily_search_api_key
            TWELVE_DATA_API_KEY=your_twelve_data_api_key
            FINNHUB_API_KEY=your_finnhub_api_key
            LANGSMITH_API_KEY=your_langsmith_key   # Optional
            ```
            """
        )