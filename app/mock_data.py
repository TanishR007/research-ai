"""Mock data provider for Stock Intelligence Terminal demo mode."""

from datetime import datetime, timezone, date
from models.state import ResearchState
from models.company import CompanyIdentity, AssetType
from models.market import MarketData
from models.news import NewsData, NewsArticle
from models.analysis import NewsEvent, ImpactAnalysis
from models.financials import FinancialData
from models.movement import MovementAnalysis
from models.evidence import Claim, ClaimType
from models.report import ResearchReport, StockPerspective, InvestmentView


def get_mock_research_state(query: str) -> ResearchState:
    """Returns a realistic, high-fidelity ResearchState for demo purposes."""
    q = query.lower()

    if "nvda" in q or "nvidia" in q:
        return _get_nvda_mock(query)
    elif "aapl" in q or "apple" in q:
        return _get_aapl_mock(query)
    elif "tsla" in q or "tesla" in q:
        return _get_tsla_mock(query)
    else:
        return _get_generic_mock(query)


def _get_nvda_mock(query: str) -> ResearchState:
    company = CompanyIdentity(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        exchange="NASDAQ",
        country="United States",
        asset_type=AssetType.STOCK,
    )

    market_data = MarketData(
        ticker="NVDA",
        price=138.45,
        change=-4.85,
        percent_change=-3.38,
        volume=54820100,
        currency="$",
        timestamp=1730284800,
    )

    financial_data = FinancialData(
        ticker="NVDA",
        market_cap=3420000000000,
        pe_ratio=48.2,
        pb_ratio=38.6,
        net_margin=0.552,
        operating_margin=0.621,
        debt_to_equity=0.22,
        latest_period=date(2026, 7, 31),
    )

    news_events = [
        NewsEvent(
            title="Hyperscaler Cloud Capex Projection Update",
            description="Major cloud providers raised aggregate 2026 AI infrastructure capex budgets by 18%, reinforcing near-term Blackwell GPU demand.",
            source_url="https://www.reuters.com/technology/nvidia-blackwell-demand-capex-2026",
            published_at=datetime(2026, 10, 29, 14, 30, tzinfo=timezone.utc),
        ),
        NewsEvent(
            title="Export Restriction Clarification on Advanced Accelerators",
            description="Regulatory agencies issued revised packaging guidelines on compute threshold ceilings for foreign enterprise shipments.",
            source_url="https://www.bloomberg.com/news/articles/2026-10-28/us-chip-packaging-export-guidance",
            published_at=datetime(2026, 10, 28, 9, 15, tzinfo=timezone.utc),
        ),
        NewsEvent(
            title="Blackwell Ultra Architecture Ramp Ahead of Schedule",
            description="Supply chain checks confirm CoWoS packaging yields improved 12% quarter-over-quarter at key foundry partners.",
            source_url="https://www.wsj.com/tech/nvidia-semiconductor-supply-chain-ramp",
            published_at=datetime(2026, 10, 27, 16, 45, tzinfo=timezone.utc),
        ),
    ]

    movement_analysis = MovementAnalysis(
        answer="NVDA dropped 3.38% primarily due to broader semiconductor sector profit-taking following revised export packaging guidance, coupled with elevated options expiry volatility across mega-cap tech.",
        contributing_factors=[
            "Sector-wide tech rotation following recent multi-week all-time highs",
            "Heightened scrutiny over foreign shipment compliance for custom accelerators",
            "Pre-earnings consolidation as institutional funds balance mega-cap risk weighting",
        ],
        supporting_evidence=[
            "Philadelphia Semiconductor Index (SOX) declined 2.8% on the same trading session",
            "Options volume spiked 40% above 30-day average near the $140 strike",
            "No company-specific reduction in revenue guidance or order cancellations was reported",
        ],
        uncertainties=[
            "Exact impact of packaging compliance rules on Q4 shipment volumes remains unquantified",
            "Extent to which intraday selling was algorithmic hedging vs. institutional rebalancing",
        ],
        sources=[
            "https://www.reuters.com/markets/us/semiconductor-index-tech-pullback-today",
            "https://www.bloomberg.com/markets/options-flows-mega-cap-tech",
        ],
    )

    analysis = ImpactAnalysis(
        summary="NVIDIA retains dominant market share (>85%) in AI compute clusters with industry-leading 55% net margins. While regulatory uncertainties introduce short-term friction, hyper-scaler capex commitments remain exceptionally robust.",
        positive_factors=[
            "Hyperscaler cloud capex expanded 18% YoY across top 4 customers",
            "Blackwell production yield improvements easing previously constrained supply",
            "Operating margin remains elite at 62.1% reflecting unmatched software moat (CUDA)",
        ],
        negative_factors=[
            "High valuation multiple (48.2x P/E) leaves minimal margin for shipment delays",
            "Ongoing regulatory overhead regarding custom chip export compliance",
        ],
        neutral_factors=[
            "Broader semiconductor sector multiple compression during macro rate reassessments",
        ],
    )

    claims = [
        Claim(
            statement="Trading volume reached 54.8M shares as price closed at $138.45 (-3.38%).",
            claim_type=ClaimType.MARKET,
            source_urls=[],
        ),
        Claim(
            statement="Trailing twelve-month Net Profit Margin stands at 55.2% with Debt-to-Equity at a conservative 0.22.",
            claim_type=ClaimType.FUNDAMENTAL,
            source_urls=[],
        ),
        Claim(
            statement="Supply chain data indicates CoWoS advanced packaging yields improved 12% QoQ.",
            claim_type=ClaimType.NEWS,
            source_urls=["https://www.wsj.com/tech/nvidia-semiconductor-supply-chain-ramp"],
        ),
        Claim(
            statement="Tier-1 cloud hyperscalers expanded aggregate AI capex forecasts by 18% for the upcoming fiscal period.",
            claim_type=ClaimType.NEWS,
            source_urls=["https://www.reuters.com/technology/nvidia-blackwell-demand-capex-2026"],
        ),
        Claim(
            statement="Consensus Wall Street analyst price target remains $165.00 with Overweight rating maintained.",
            claim_type=ClaimType.ANALYST,
            source_urls=["https://www.bloomberg.com/markets/analyst-ratings-nvda"],
        ),
    ]

    perspective = StockPerspective(
        overall_view=InvestmentView.CAUTIOUSLY_BULLISH,
        confidence=0.82,
        reasoning="Despite short-term volatility from regulatory headlines and tech sector rebalancing, NVIDIA's structural pricing power and datacenter expansion remain uncompromised. The recent 3.4% dip is characteristic of macro positioning rather than fundamental degradation.",
        positive_factors=[
            "Irreplaceable CUDA ecosystem moat locking in hyperscaler workloads",
            "Acceleration in Blackwell Ultra shipments with expanding foundry allocation",
            "Exceptional return on invested capital and zero liquidity stress",
        ],
        negative_factors=[
            "Elevated multiple makes stock sensitive to minor packaging or shipment delays",
            "Geopolitical export friction creates periodic sentiment overhang",
        ],
        key_risks=[
            "Potential enforcement of tighter compute density ceilings in international markets",
            "Hyperscaler internal silicon (ASIC/TPU) adoption over multi-year horizon",
        ],
        key_uncertainties=[
            "Duration of macro semiconductor multiple compression",
            "Near-term gross margin trajectory during early Blackwell production transition",
        ],
        catalysts_to_watch=[
            "Upcoming quarterly earnings release and Q1 datacenter revenue guidance",
            "Hyperscaler Q3 capital expenditure commentary",
            "GTC product roadmap announcements",
        ],
    )

    report = ResearchReport(
        executive_summary="NVIDIA Corporation ($NVDA) remains the premier compute engine for the generative AI paradigm. While shares fell 3.38% in the latest session, our cross-agent intelligence establishes that this move was driven by sector-wide options positioning and regulatory headlines rather than deterioration in end-customer demand.",
        market_snapshot="NVDA is trading at $138.45 (-3.38%) on above-average volume of 54.8M shares. Market cap remains steady at $3.42T, supported by exceptional 62.1% operating margins and a healthy 0.22 Debt-to-Equity profile.",
        recent_developments=[
            "Blackwell Ultra packaging yields registered double-digit efficiency gains at foundry partners.",
            "Revised export documentation clarified packaging requirements without impacting core domestic backlog.",
            "Global enterprise AI infrastructure spending grew 18% YoY.",
        ],
        positive_factors=[
            "Massive forward order visibility spanning multiple fiscal quarters",
            "Elite profitability metrics with net profit margin exceeding 55%",
            "Enterprise software monetization ramping across NVIDIA AI Enterprise suite",
        ],
        negative_factors=[
            "Elevated valuation requiring consistent top-line beats",
            "Sensitivity to geopolitical packaging regulations",
        ],
        uncertainties=[
            "Pace of international enterprise compliance approvals",
            "Long-term custom ASIC substitution rates",
        ],
        key_claims=[
            "Net margin sustained at 55.2% over trailing twelve months",
            "Cloud hyperscaler capex expanded 18% YoY",
            "Consensus analyst targets cluster around $165.00",
        ],
        sources=[
            "https://www.reuters.com/technology/nvidia-blackwell-demand-capex-2026",
            "https://www.wsj.com/tech/nvidia-semiconductor-supply-chain-ramp",
            "https://www.bloomberg.com/news/articles/2026-10-28/us-chip-packaging-export-guidance",
        ],
    )

    return ResearchState(
        query=query,
        company=company,
        market_data=market_data,
        financial_data=financial_data,
        news_events=news_events,
        movement_analysis=movement_analysis,
        analysis=analysis,
        claims=claims,
        perspective=perspective,
        report=report,
    )


def _get_aapl_mock(query: str) -> ResearchState:
    company = CompanyIdentity(
        ticker="AAPL",
        company_name="Apple Inc.",
        exchange="NASDAQ",
        country="United States",
        asset_type=AssetType.STOCK,
    )

    market_data = MarketData(
        ticker="AAPL",
        price=234.80,
        change=4.20,
        percent_change=1.82,
        volume=48320000,
        currency="$",
        timestamp=1730284800,
    )

    financial_data = FinancialData(
        ticker="AAPL",
        market_cap=3580000000000,
        pe_ratio=33.4,
        pb_ratio=54.2,
        net_margin=0.264,
        operating_margin=0.312,
        debt_to_equity=1.45,
        latest_period=date(2026, 6, 30),
    )

    news_events = [
        NewsEvent(
            title="Apple Intelligence Rollout Drives Smartphone Upgrade Cycle",
            description="Carrier upgrade rates increased 14% month-over-month as on-device AI features drove accelerated premium device trade-ins.",
            source_url="https://www.bloomberg.com/news/apple-intelligence-carrier-upgrades",
            published_at=datetime(2026, 10, 29, 11, 0, tzinfo=timezone.utc),
        ),
        NewsEvent(
            title="Services Revenue Accelerates Beyond $25B Quarterly Run-Rate",
            description="App Store, iCloud, and Apple Pay revenue reached record gross margins of 74%, expanding overall blended corporate margins.",
            source_url="https://www.wsj.com/tech/apple-services-record-margins",
            published_at=datetime(2026, 10, 28, 15, 20, tzinfo=timezone.utc),
        ),
    ]

    analysis = ImpactAnalysis(
        summary="Apple demonstrates remarkable ecosystem retention with high-margin Services revenue offsetting hardware cycle maturation. The rollout of Apple Intelligence has revitalized consumer upgrade momentum.",
        positive_factors=[
            "Services segment gross margins expanded to 74% with double-digit subscriber growth",
            "Apple Intelligence integration triggering multi-year device upgrade super-cycle",
            "Immense capital return program ($100B+ annual share repurchases)",
        ],
        negative_factors=[
            "Greater China smartphone competitive intensity from local OEM flagships",
            "Regulatory antitrust inquiries regarding App Store fee structures in EU/US",
        ],
        neutral_factors=[],
    )

    perspective = StockPerspective(
        overall_view=InvestmentView.BULLISH,
        confidence=0.88,
        reasoning="Apple combines fortress balance sheet cash flows with an expanding 2.2B active device installed base. The inflection in Services recurring revenue and consumer AI monetization supports premium valuation durability.",
        positive_factors=[
            "2.2B active device installed base driving frictionless recurring Services expansion",
            "Accelerating replacement cadence spurred by generative AI features",
            "Unrivaled free cash flow generation exceeding $100B annually",
        ],
        negative_factors=[
            "Regulatory compliance friction in European Union markets",
            "P/E ratio of 33.4x is near 5-year upper percentile",
        ],
        key_risks=[
            "App Store revenue take-rate revisions mandated by regulatory courts",
            "Macro consumer discretionary spending pullback in key regional markets",
        ],
        key_uncertainties=[
            "Sustained retention velocity for premium AI tier subscriptions",
        ],
        catalysts_to_watch=[
            "Upcoming Q4 holiday quarter revenue guidance and iPhone ASP data",
            "Developer conference updates on third-party AI assistant integrations",
        ],
    )

    claims = [
        Claim(
            statement="AAPL closed up +1.82% at $234.80 on 48.3M shares volume.",
            claim_type=ClaimType.MARKET,
            source_urls=[],
        ),
        Claim(
            statement="Services revenue quarterly run-rate exceeded $25B with 74% gross margin.",
            claim_type=ClaimType.FUNDAMENTAL,
            source_urls=["https://www.wsj.com/tech/apple-services-record-margins"],
        ),
        Claim(
            statement="Carrier upgrade rates increased 14% MoM following Apple Intelligence deployment.",
            claim_type=ClaimType.NEWS,
            source_urls=["https://www.bloomberg.com/news/apple-intelligence-carrier-upgrades"],
        ),
    ]

    report = ResearchReport(
        executive_summary="Apple Inc. ($AAPL) exhibits strong operational momentum as consumer interest in Apple Intelligence accelerates premium upgrade cycles. Services division growth continues to structurally elevate corporate gross margins.",
        market_snapshot="Trading at $234.80 (+1.82%) with a market capitalization of $3.58T. Valuation trades at 33.4x TTM P/E with operating margins at 31.2%.",
        recent_developments=[
            "Global carrier activation metrics reveal double-digit increases in flagship trade-ins.",
            "Record quarterly Services segment run-rate reported across subscriptions.",
        ],
        positive_factors=[
            "Installed base growth reaching all-time highs across all geographic segments",
            "Expanding software subscription revenue mix",
        ],
        negative_factors=[
            "Regulatory scrutiny on default search engine partnerships and App Store commissions",
        ],
        uncertainties=[
            "Elasticity of consumer smartphone upgrade cycles over a 12-month window",
        ],
        key_claims=[
            "Services gross margin exceeds 74%",
            "Active device installed base surpasses 2.2B units",
        ],
        sources=[
            "https://www.bloomberg.com/news/apple-intelligence-carrier-upgrades",
            "https://www.wsj.com/tech/apple-services-record-margins",
        ],
    )

    return ResearchState(
        query=query,
        company=company,
        market_data=market_data,
        financial_data=financial_data,
        news_events=news_events,
        analysis=analysis,
        claims=claims,
        perspective=perspective,
        report=report,
    )


def _get_tsla_mock(query: str) -> ResearchState:
    company = CompanyIdentity(
        ticker="TSLA",
        company_name="Tesla, Inc.",
        exchange="NASDAQ",
        country="United States",
        asset_type=AssetType.STOCK,
    )

    market_data = MarketData(
        ticker="TSLA",
        price=218.60,
        change=-2.80,
        percent_change=-1.26,
        volume=68410000,
        currency="$",
        timestamp=1730284800,
    )

    financial_data = FinancialData(
        ticker="TSLA",
        market_cap=695000000000,
        pe_ratio=62.8,
        pb_ratio=10.4,
        net_margin=0.082,
        operating_margin=0.098,
        debt_to_equity=0.11,
        latest_period=date(2026, 6, 30),
    )

    news_events = [
        NewsEvent(
            title="Energy Storage Deployment Ramps 85% YoY",
            description="Tesla Megapack installations reached record megawatt-hour volume, providing high-margin operational cash flow support.",
            source_url="https://www.reuters.com/business/autos-transportation/tesla-energy-storage-megapack-record",
            published_at=datetime(2026, 10, 28, 14, 0, tzinfo=timezone.utc),
        ),
        NewsEvent(
            title="FSD Unsupervised Testing Permitting Progress",
            description="Regulatory filings in key states show advancing safety validation submissions for unsupervised autonomous commercial ride-hailing.",
            source_url="https://www.bloomberg.com/news/tesla-fsd-commercial-permitting",
            published_at=datetime(2026, 10, 27, 10, 30, tzinfo=timezone.utc),
        ),
    ]

    perspective = StockPerspective(
        overall_view=InvestmentView.NEUTRAL,
        confidence=0.68,
        reasoning="Tesla is in a pivotal transition phase between automotive volume normalization and long-term autonomy monetization. While automotive gross margins face price competition, Energy Storage segment expansion provides valuable operational diversification.",
        positive_factors=[
            "Explosive growth in Energy Megapack division with industry-leading margins",
            "Pioneering autonomous vehicle compute and vision training infrastructure",
            "Virtually debt-free balance sheet with over $30B in liquid cash reserves",
        ],
        negative_factors=[
            "Automotive gross margins pressured by global EV price discounting",
            "High valuation multiple (62.8x P/E) heavily reliant on autonomy execution",
        ],
        key_risks=[
            "Regulatory delays in commercial robotaxi driverless deployment approvals",
            "Intensified global EV competition in European and Asian markets",
        ],
        key_uncertainties=[
            "Timing and regulatory monetization timeline for unsupervised FSD",
        ],
        catalysts_to_watch=[
            "Upcoming regulatory safety data filings for commercial driverless rides",
            "Next generation low-cost consumer platform production timelines",
        ],
    )

    return ResearchState(
        query=query,
        company=company,
        market_data=market_data,
        financial_data=financial_data,
        news_events=news_events,
        analysis=ImpactAnalysis(
            summary="Tesla's business model is diversifying rapidly into energy storage and autonomous AI architectures, offsetting automotive margin headwinds.",
            positive_factors=["Energy Megapack volume +85% YoY", "Unsupervised autonomy regulatory milestones"],
            negative_factors=["Auto gross margins compressed to ~17%"],
            neutral_factors=["Global vehicle deliveries tracking within expectations"],
        ),
        claims=[
            Claim(
                statement="TSLA traded down -1.26% at $218.60 on 68.4M shares volume.",
                claim_type=ClaimType.MARKET,
                source_urls=[],
            ),
            Claim(
                statement="Energy storage installations surged 85% year-over-year.",
                claim_type=ClaimType.NEWS,
                source_urls=["https://www.reuters.com/business/autos-transportation/tesla-energy-storage-megapack-record"],
            ),
        ],
        perspective=perspective,
        report=ResearchReport(
            executive_summary="Tesla, Inc. ($TSLA) is balancing core EV production optimization with aggressive AI and energy infrastructure scale. While near-term auto margins reflect competitive pricing, the energy division is emerging as a premier profit engine.",
            market_snapshot="Current price $218.60 (-1.26%) with $695B market cap and 62.8x P/E ratio.",
            recent_developments=["Megapack energy deployments set all-time quarterly records."],
            positive_factors=["Energy division scaling", "Autonomous compute advancements"],
            negative_factors=["Auto pricing pressure"],
            uncertainties=["FSD regulatory approval timing"],
            key_claims=["Megapack installations +85% YoY"],
            sources=["https://www.reuters.com/business/autos-transportation/tesla-energy-storage-megapack-record"],
        ),
    )


def _get_generic_mock(query: str) -> ResearchState:
    ticker = query.strip().split()[0].upper() if query.strip() else "DEMO"
    ticker = ticker.replace("?", "").replace("!", "")[:5]

    company = CompanyIdentity(
        ticker=ticker,
        company_name=f"{ticker} Global Intelligence",
        exchange="NYSE",
        country="United States",
        asset_type=AssetType.STOCK,
    )

    market_data = MarketData(
        ticker=ticker,
        price=185.20,
        change=2.45,
        percent_change=1.34,
        volume=24500000,
        currency="$",
        timestamp=1730284800,
    )

    financial_data = FinancialData(
        ticker=ticker,
        market_cap=210000000000,
        pe_ratio=24.5,
        pb_ratio=6.2,
        net_margin=0.185,
        operating_margin=0.228,
        debt_to_equity=0.45,
        latest_period=date(2026, 6, 30),
    )

    news_events = [
        NewsEvent(
            title=f"{ticker} Announces Strategic Cloud & AI Integration",
            description=f"Enterprise adoption metrics beat expectations with quarterly expansion across Fortune 500 accounts.",
            source_url="https://www.reuters.com/business/technology/enterprise-ai-growth",
            published_at=datetime(2026, 10, 29, 12, 0, tzinfo=timezone.utc),
        ),
    ]

    perspective = StockPerspective(
        overall_view=InvestmentView.CAUTIOUSLY_BULLISH,
        confidence=0.76,
        reasoning=f"{ticker} displays steady operational execution, solid return on equity, and expanding software subscription margins amidst favorable secular industry trends.",
        positive_factors=["Accelerating enterprise contract wins", "Net margin expanded to 18.5%"],
        negative_factors=["Macro sensitivity in consumer-facing lines"],
        key_risks=["Potential FX foreign currency headwinds"],
        key_uncertainties=["Pace of international enterprise adoption"],
        catalysts_to_watch=["Next quarterly financial disclosures and guidance revision"],
    )

    return ResearchState(
        query=query,
        company=company,
        market_data=market_data,
        financial_data=financial_data,
        news_events=news_events,
        analysis=ImpactAnalysis(
            summary=f"Fundamental health for {ticker} remains positive with double-digit operating margins and modest debt leverage.",
            positive_factors=["Healthy 22.8% operating margins", "Strong free cash flow generation"],
            negative_factors=["Valuation is in line with historical median"],
            neutral_factors=[],
        ),
        claims=[
            Claim(
                statement=f"{ticker} closed at $185.20 (+1.34%) with 24.5M shares traded.",
                claim_type=ClaimType.MARKET,
                source_urls=[],
            ),
        ],
        perspective=perspective,
        report=ResearchReport(
            executive_summary=f"Comprehensive intelligence assessment for {ticker}. The company maintains sound balance sheet metrics, robust margin defense, and constructive positioning across core business lines.",
            market_snapshot=f"Price: $185.20 | Change: +1.34% | Volume: 24.5M | P/E: 24.5x",
            recent_developments=["Enterprise revenue growth and margin expansion."],
            positive_factors=["Balance sheet strength", "Positive operating margin momentum"],
            negative_factors=["Macro cycle exposure"],
            uncertainties=["International enterprise adoption velocity"],
            key_claims=[f"{ticker} operating margin stands at 22.8%"],
            sources=["https://www.reuters.com/business/technology/enterprise-ai-growth"],
        ),
    )
