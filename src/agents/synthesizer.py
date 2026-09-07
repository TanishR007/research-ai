from langchain_core.prompts import prompt
from models.state import ResearchState
from models.report import ResearchReport
from llm.client import llm

structured_llm = llm.with_structured_output(ResearchReport)

def syntesize_report(state: ResearchState) -> dict:

    if state.company is None:
        return {
            "errors": ["Cannot synthesize report: company not resolved"]
        }
    
    prompt = f"""
    You are a financial research report synthesizer.

    Create a concise research report about the company using ONLY
    the information supplied below.

    COMPANY:
    {state.company}

    MARKET DATA:
    {state.market_data}

    FUNDAMENTAL DATA:
    {state.financial_data}

    NEWS EVENTS:
    {state.news_events}

    IMPACT ANALYSIS:
    {state.analysis}

    EXTRACTED CLAIMS:
    {state.claims}


    RULES:

    1. Do not invent facts, numbers, events, dates, or sources.

    2. Do not introduce information that is not present in the
    supplied research.

    3. Clearly distinguish factual information from interpretation.

    4. Do not claim that an event caused a stock movement unless
    the supplied evidence explicitly establishes causation.

    5. Analyst opinions are opinions, not established facts.

    6. Analyst price targets are expectations, not guaranteed
    future prices.

    7. If the supplied information is insufficient to establish
    something, explicitly state that uncertainty.

    8. The report should synthesize the research rather than
    simply repeat every piece of raw data.

    9. Preserve important numerical information where relevant.

    10. Include the supplied source URLs associated with claims
        and news events. Do not invent URLs.

    Structure the report around:

    - Executive summary
    - Market snapshot
    - Recent developments
    - Positive factors
    - Negative factors
    - Uncertainties
    - Key claims
    - Sources

    The report should prioritize interpretation and relationships
    between the supplied facts rather than simply listing them.

    For each major development, explain its potential relevance
    when the supplied information supports doing so.

    Do not assign positive or negative significance to an event
    unless the supplied analysis provides a basis for doing so.

    Return ONLY the structured report.
    """

    try:
        result = structured_llm.invoke(prompt)

        return{
            "report": result
        }
    except Exception as e:
        return {
            "errors": [f"Report synthesis failed: {str(e)}"]
        }