from models.state import ResearchState
from graph.workflow import workflow


def run_research(query: str) -> ResearchState:
    """
    Run the complete stock research workflow.

    Args:
        query: User's stock/company research query.

    Returns:
        Final ResearchState produced by LangGraph.
    """

    if not query or not query.strip():
        raise ValueError("Research query cannot be empty.")

    initial_state = ResearchState(
        query=query.strip()
    )

    result = workflow.invoke(initial_state)

    return ResearchState.model_validate(result)