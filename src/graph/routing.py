from models.state import ResearchState

def route_after_ticker_resolution(state: ResearchState):
    if state.company is None:
        return "end"
    return ["market", "news", "fundamentals"]
    
def route_after_analysis(state: ResearchState):

    query = state.query.lower()

    movement_terms = [
        "why did",
        "why is",
        "why was",
        "fall",
        "fell",
        "drop",
        "dropped",
        "decline",
        "declined",
        "down",
        "rise",
        "rose",
        "rising",
        "jump",
        "jumped",
        "surge",
        "surged",
        "rally",
        "rallied",
        "gain",
        "gained",
        "up",
        "movement",
        "moving",
        "crash",
        "plunge",
        "plunged",
    ]

    if any(term in query for term in movement_terms):
        return "movement"

    return "normal"