"""Styles and Design System for Stock Intelligence Streamlit Application."""

GLOBAL_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Root Theme Variables */
:root {
    --bg-primary: #070B14;
    --bg-card: rgba(15, 23, 42, 0.72);
    --bg-card-hover: rgba(30, 41, 59, 0.85);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-focus: rgba(56, 189, 248, 0.4);
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --emerald-glow: #10B981;
    --emerald-bg: rgba(16, 185, 129, 0.12);
    --rose-glow: #F43F5E;
    --rose-bg: rgba(244, 63, 94, 0.12);
    --cyan-glow: #06B6D4;
    --cyan-bg: rgba(6, 182, 212, 0.12);
    --amber-glow: #F59E0B;
    --amber-bg: rgba(245, 158, 11, 0.12);
    --purple-glow: #A855F7;
    --purple-bg: rgba(168, 85, 247, 0.12);
}

/* Global Page Background & Fonts */
.stApp {
    background: radial-gradient(circle at 15% 10%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 30%, rgba(99, 102, 241, 0.07) 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(16, 185, 129, 0.05) 0%, transparent 50%),
                #070B14 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Streamlit Header & Navigation overrides */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Main Container spacing */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

/* Search input container */
div[data-testid="stTextInput"] > div > div > input {
    background: rgba(15, 23, 42, 0.8) !important;
    color: #F8FAFC !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 14px 20px !important;
    font-size: 1.05rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-shadow: 0 4px 24px -2px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2), 0 4px 24px -2px rgba(0, 0, 0, 0.4) !important;
}

/* Primary Button Styling */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 50%, #6366F1 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.8rem !important;
    font-size: 1rem !important;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(59, 130, 246, 0.55) !important;
}

div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.6) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 20px !important;
    padding: 0.25rem 0.85rem !important;
    font-size: 0.82rem !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    color: var(--text-primary) !important;
    border-color: rgba(56, 189, 248, 0.5) !important;
    background: rgba(30, 41, 59, 0.9) !important;
}

/* Tabs Styling */
div[data-testid="stTabs"] {
    margin-top: 1.5rem !important;
}

button[data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.75rem 1.25rem !important;
    transition: all 0.2s ease !important;
}

button[data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #38BDF8 !important;
    border-bottom: 2px solid #38BDF8 !important;
    background: transparent !important;
}

/* Glassmorphic Cards & Containers */
.glass-panel {
    background: var(--bg-card);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    transition: border-color 0.25s ease, transform 0.25s ease;
}

.glass-panel:hover {
    border-color: rgba(255, 255, 255, 0.15);
}

/* Hero Header Card */
.hero-header {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-header::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 250px;
    height: 100%;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.1) 0%, transparent 70%);
    pointer-events: none;
}

/* Metrics Strip Grid */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.25rem;
    transition: all 0.25s ease;
}

.metric-card:hover {
    border-color: rgba(56, 189, 248, 0.3);
    transform: translateY(-2px);
}

.metric-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.35rem;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.badge-bullish {
    background: var(--emerald-bg);
    color: var(--emerald-glow);
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-bearish {
    background: var(--rose-bg);
    color: var(--rose-glow);
    border: 1px solid rgba(244, 63, 94, 0.3);
}

.badge-neutral {
    background: var(--amber-bg);
    color: var(--amber-glow);
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-cyan {
    background: var(--cyan-bg);
    color: var(--cyan-glow);
    border: 1px solid rgba(6, 182, 212, 0.3);
}

.badge-purple {
    background: var(--purple-bg);
    color: var(--purple-glow);
    border: 1px solid rgba(168, 85, 247, 0.3);
}

/* Movement Callout Box */
.movement-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
    border-left: 4px solid #38BDF8;
    border-radius: 0 16px 16px 0;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

/* Factor Cards */
.factor-card {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    border-left: 3px solid transparent;
    transition: all 0.2s ease;
}

.factor-positive {
    border-left-color: var(--emerald-glow);
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.06) 0%, rgba(15, 23, 42, 0.6) 100%);
}

.factor-negative {
    border-left-color: var(--rose-glow);
    background: linear-gradient(90deg, rgba(244, 63, 94, 0.06) 0%, rgba(15, 23, 42, 0.6) 100%);
}

.factor-uncertain {
    border-left-color: var(--amber-glow);
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.06) 0%, rgba(15, 23, 42, 0.6) 100%);
}

/* Claim & Source Pills */
.claim-card {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.2rem 0.6rem;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    font-size: 0.75rem;
    color: #38BDF8;
    text-decoration: none;
    margin-right: 0.5rem;
    margin-top: 0.35rem;
    transition: all 0.2s ease;
}

.source-chip:hover {
    border-color: #38BDF8;
    color: #7DD3FC;
    transform: translateY(-1px);
}

/* Pulse Dot */
.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
}

/* Spinner styling */
div[data-testid="stSpinner"] {
    color: #38BDF8 !important;
}
</style>
"""
