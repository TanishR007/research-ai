from models.state import ResearchState
from models.analysis import ImpactAnalysis
from llm.client import llm


structured_llm = llm.with_structured_output(ImpactAnalysis)


def analyze_research(state: ResearchState) -> dict:
    if state.company is None:
        return {
            "errors": ["Cannot perform analysis: company not resolved"]
        }

    events_context = []

    for event in state.news_events:
        events_context.append(
            {
                "title": event.title,
                "description": event.description,
                "published_at": (
                    event.published_at.isoformat()
                    if event.published_at
                    else None
                ),
                "source_url": event.source_url,
            }
        )

    prompt = f"""
You are a financial impact analysis agent.

Analyze the following information for
{state.company.company_name} ({state.company.ticker}).

USER QUERY:
{state.query}

MARKET DATA:
{state.market_data}

FUNDAMENTAL DATA:
{state.financial_data}

EXTRACTED NEWS EVENTS:
{events_context}

Your task is to identify meaningful factors that may
help explain the company's current situation.

Rules:

1. Base your analysis ONLY on the supplied information.
2. Distinguish facts from interpretations.
3. Do not invent facts.
4. Do not claim that an event caused a stock movement
   unless the supplied evidence explicitly establishes causation.
5. Do not treat analyst opinions or price targets as facts.
6. Do not treat forecasts as established outcomes.
7. If the evidence is insufficient to explain the stock movement,
   explicitly say so.
8. Positive and negative factors should be based on the supplied
   evidence.
9. Do not extract or create new news events.
10. The extracted news events are already available separately;
    focus only on analyzing their potential relevance.

A factor should only be classified as positive or negative when
the supplied evidence supports that interpretation.

Do not classify an event as negative merely because it sounds negative.

For example, an insider sale under a pre-scheduled Rule 10b5-1 plan
should not automatically be treated as a negative factor.

If the direction of an event's impact is uncertain, classify it
as neutral or explain the uncertainty in the summary.

Return a structured impact analysis.
"""

    try:
        analysis = structured_llm.invoke(prompt)

        return {
            "analysis": analysis
        }

    except Exception as e:
        return {
            "errors": [f"Analysis failed: {str(e)}"]
        }