# ⚡ Stock Intelligence Terminal (`research-ai`)

> **Institutional-grade, multi-agent financial research & market intelligence engine** powered by **LangGraph**, **Google Gemini**, **TwelveData**, **Finnhub**, **Tavily**, and **Plotly**.

---

## 🌟 Overview

**Stock Intelligence Terminal** transforms natural language questions about public equities (e.g., *"Why did NVDA fall today?"*, *"AAPL developments"*, or *"TSLA fundamental valuation"*) into institutional-grade equity research reports.

### ✨ Key Features
- **⚡ Multi-Agent Swarm (LangGraph):** Orchestrates specialized agents for ticker resolution, market quotes, financial fundamentals, news event extraction, and synthesis.
- **🛡️ Strict Factual Grounding:** Built with anti-hallucination guardrails. Separates raw facts from analyst speculation, maps verifiable claims, and links directly to primary sources.
- **📊 Real-Time Market & Fundamental Analysis:** Fetches live intraday prices, volume, P/E, P/B, operating/net margins, and debt ratios.
- **🎯 AI Sentiment Speedometer:** Radial gauge visualizing analyst sentiment (`BEARISH` to `BULLISH`) with a calibrated AI confidence score.
- **⚡ Dedicated Movement Analysis:** Specialized agent investigating reasons behind recent price moves without premature or unverified causation claims.
- **🎮 Built-In Demo Simulation Mode:** Test the entire interface and workflows immediately—**no API keys required**!

---

## 🏗️ Architecture

```mermaid
flowchart TD
    Start([User Query]) --> ResolveTicker[1. Resolve Ticker]
    ResolveTicker --> RouteCheck{Company Found?}
    RouteCheck -- No --> EndNode([End / Error])
    RouteCheck -- Yes: Parallel Fan-out --> MarketData[2a. Market Data (TwelveData)]
    RouteCheck -- Yes: Parallel Fan-out --> News[2b. News Search (Tavily)]
    RouteCheck -- Yes: Parallel Fan-out --> Fundamentals[2c. Fundamentals (Finnhub)]
    
    News --> NewsEvents[3. Extract Concrete News Events]
    MarketData --> Analysis[4. Impact Analysis]
    NewsEvents --> Analysis
    Fundamentals --> Analysis
    
    Analysis --> RouteMovement{Movement Query?}
    RouteMovement -- Yes --> MovementAnalysis[5. Movement Analysis]
    RouteMovement -- No --> ClaimExtraction[6. Verifiable Claim Extraction]
    MovementAnalysis --> ClaimExtraction
    
    ClaimExtraction --> Synthesizer[7. Synthesize Report]
    Synthesizer --> Perspective[8. AI Investment Perspective]
    Perspective --> StreamlitUI([Modern Dark Terminal UI])
```

---

## 🚀 Quick Start & Setup Guide

### 1. Prerequisites
- **Python:** Version `>= 3.10` (Python 3.12+ or 3.14 recommended)
- **Package Manager:** [`uv`](https://docs.astral.sh/uv/) (recommended for instant installs) or standard `pip`

---

### 2. Clone the Repository
```bash
git clone https://github.com/TanishR007/research-ai.git
cd research-ai
```

---

### 3. Install Dependencies

#### Option A: Using `uv` (Recommended)
```bash
# Install uv if you don't have it:
# curl -LsSf https://astral.sh/uv/install.sh | sh  (macOS/Linux)
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" (Windows)

uv sync
```

#### Option B: Using standard `pip` & virtual environment
```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables (Optional for Demo Mode)

Copy the example environment file to create your `.env`:

```bash
# Windows (PowerShell):
Copy-Item .env.example .env

# macOS / Linux:
cp .env.example .env
```

Open `.env` and insert your API keys:

```env
# 1. Google Gemini (Required for LLM extraction and synthesis)
# Obtain free at: https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key

# 2. Tavily Search (Required for real-time web & news search)
# Obtain free at: https://tavily.com/
TAVILY_API_KEY=your_tavily_api_key

# 3. Twelve Data (Required for live stock quotes & symbol search)
# Obtain free at: https://twelvedata.com/
TWELVE_DATA_API_KEY=your_twelve_data_api_key

# 4. Finnhub (Required for company fundamentals & ratios)
# Obtain free at: https://finnhub.io/
FINNHUB_API_KEY=your_finnhub_api_key

# 5. LangSmith (Optional: for workflow tracing & observability)
# https://smith.langchain.com/
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=stock-intelligence-ai
```

> 💡 **No API keys right now? No problem!**  
> The terminal includes a **Demo Simulation Mode** that is enabled automatically when keys are not configured. You can fully test the application with realistic simulated multi-agent data right away.

---

### 5. Launch the Application

Run the Streamlit application:

```bash
# Using uv:
uv run streamlit run app/streamlit_app.py

# Or using standard python virtual environment:
streamlit run app/streamlit_app.py
```

Once running, navigate in your browser to:
👉 **`http://localhost:8501`**

---

## 🎮 How to Use the Terminal

1. **Quick Prompts:** Click on any of the quick prompt chips at the top:
   - `🔥 NVDA: Why did it drop?`
   - `🍎 AAPL: Developments`
   - `⚡ TSLA: Valuation & Margins`
   - `💻 MSFT`
   - `📦 AMZN`
2. **Custom Query:** Type any ticker or research question in the search bar (e.g., `"Why did Google rise?"`, `"AMD earnings impact"`).
3. **Execution:** Click **Analyze ⚡** to watch the multi-agent pipeline animate through each agent stage.
4. **Explore the Results:**
   - **Hero Card:** Ticker, exchange, country, and price change badge.
   - **KPI Grid:** Live price, trading volume, P/E & P/B ratios, and profit margins.
   - **Movement Analysis:** Dedicated breakdown for price move questions.
   - **Tab 1 (AI Perspective):** Interactive Plotly radial speedometer gauge and factor balance bar.
   - **Tab 2 (Factor Matrix):** Side-by-side positive catalysts vs. negative risks and fundamental metrics chart.
   - **Tab 3 (Verified Claims):** Auditable claims categorized by type (`MARKET`, `NEWS`, `FUNDAMENTAL`, `ANALYST`) with clickable source links.
   - **Tab 4 (Institutional Report):** Comprehensive executive summary and recent developments.
5. **Switch Modes:** Use the toggle in the upper right corner to switch between **Demo Simulation Mode** and **Live API Mode** at any time.

---

## 📁 Project Structure

```
research-ai/
├── app/
│   ├── streamlit_app.py       # Main Streamlit application and layout
│   ├── styles.py              # Dark glassmorphic design system (CSS)
│   ├── components.py          # HTML/CSS custom cards (Hero, KPIs, Claims)
│   ├── charts.py              # Interactive Plotly visualizations (Gauge, Bar)
│   └── mock_data.py           # High-fidelity simulated data for Demo Mode
├── src/
│   ├── agents/
│   │   ├── ticker_resolver.py   # LLM entity extraction & TwelveData search
│   │   ├── market.py            # TwelveData live price and volume agent
│   │   ├── fundamentals.py      # Finnhub balance sheet and ratio metrics
│   │   ├── news.py              # Tavily web news retrieval
│   │   ├── event_extraction.py  # Structured news event extractor
│   │   ├── analysis.py          # Factor impact analysis agent
│   │   ├── movement_analysis.py # Price movement causation analyzer
│   │   ├── claim_extraction.py  # Grounded factual claim extractor
│   │   ├── synthesizer.py       # Institutional research report builder
│   │   └── perspective.py       # Investment perspective and confidence agent
│   ├── graph/
│   │   ├── workflow.py          # LangGraph state machine definition
│   │   └── routing.py           # Parallel fan-out and conditional edge logic
│   ├── models/                  # Pydantic state and data models
│   ├── tools/                   # API clients (TwelveData, Finnhub, Tavily)
│   ├── services/                # High-level research orchestration services
│   └── config/
│       └── settings.py          # Environment settings & validation
├── requirements.txt           # Python package requirements
├── pyproject.toml             # Project build and dependency configuration
└── .env.example               # Example API key configuration
```

---

## 🛠️ Troubleshooting

- **ModuleNotFoundError: No module named 'plotly' / 'streamlit':**  
  Ensure you are running within your activated virtual environment or using `uv run`.
- **Validation error for Settings / missing keys:**  
  Make sure you have either enabled **Demo Mode** or copied `.env.example` to `.env` with valid keys.
- **Port 8501 is already in use:**  
  Specify a custom port:
  ```bash
  uv run streamlit run app/streamlit_app.py --server.port=8502
  ```

---

## 📄 License
This project is open-source under the MIT License.
