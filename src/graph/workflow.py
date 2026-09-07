from agents.fundamentals import get_fundamentals
from langgraph.graph import StateGraph, START, END
from models.state import ResearchState
from agents.market import get_market_data
from agents.news import get_news
from agents.ticker_resolver import resolve_ticker
from graph.routing import route_after_ticker_resolution
from agents.analysis import analyze_research
from agents.event_extraction import extract_news_events
from agents.claim_extraction import extract_claims
from agents.synthesizer import syntesize_report
from agents.perspective import generate_perspective

graph_builder = StateGraph(ResearchState)
graph_builder.add_node("resolve_ticker", resolve_ticker)
graph_builder.add_node("get_market_data", get_market_data)
graph_builder.add_node("get_news", get_news)
graph_builder.add_node("get_fundamentals", get_fundamentals)
graph_builder.add_node("analysis", analyze_research)
graph_builder.add_node("extract_news_events", extract_news_events)
graph_builder.add_node("claim_extraction", extract_claims)
graph_builder.add_node("report_synthesis", syntesize_report)
graph_builder.add_node("perspective", generate_perspective)

graph_builder.add_edge(START, "resolve_ticker")
graph_builder.add_conditional_edges(
    "resolve_ticker",
    route_after_ticker_resolution,
    {
        "market": "get_market_data",
        "news": "get_news",
        "fundamentals": "get_fundamentals",
        "end": END
    }
)
graph_builder.add_edge("get_market_data", "analysis")
graph_builder.add_edge("get_news", "extract_news_events")
graph_builder.add_edge("extract_news_events", "analysis")
graph_builder.add_edge("get_fundamentals", "analysis")
graph_builder.add_edge("analysis", "claim_extraction")
graph_builder.add_edge("claim_extraction", "report_synthesis")
graph_builder.add_edge("report_synthesis", "perspective")
graph_builder.add_edge("perspective", END)

workflow = graph_builder.compile()

