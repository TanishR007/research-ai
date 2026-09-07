from models.state import ResearchState

def route_after_ticker_resolution(state: ResearchState):
    if state.company is None:
        return "end"
    return ["market", "news", "fundamentals"]
    