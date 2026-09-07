from langchain_core.prompts import prompt
from models.state import ResearchState
from models.report import StockPerspective
from llm.client import llm

structured_llm = llm.with_structured_output(StockPerspective)

def generate_perspective(state: ResearchState) -> dict:
    if state.report is None:
        return {
            "errors": ["Cannot generate perspective: report unavailable"]
        }

    prompt = f"""
    You are an investment research analyst.

    You have been given a synthesized research report.

    Your task is to form an analytical perspective about the
    company based ONLY on this report.

    COMPANY:
    {state.company}

    RESEARCH REPORT:
    {state.report}


    Your perspective must:

    1. Assess whether the overall picture is:
    - bullish
    - cautiously bullish
    - neutral
    - cautiously bearish
    - bearish

    2. Explain WHY you reached that conclusion.

    3. Identify the strongest positive factors.

    4. Identify the strongest negative factors.

    5. Identify important risks.

    6. Identify uncertainties where the available information
    does not justify a strong conclusion.

    7. Identify catalysts or developments worth watching.

    8. Base every factual statement on the supplied report.

    9. Do NOT introduce outside facts.

    10. Do NOT invent financial metrics, events, causes, or
        predictions.

    11. Do NOT treat analyst forecasts as guaranteed outcomes.

    12. Do NOT assume that a short-term stock movement represents
        the company's long-term business performance.

    13. Do NOT give personalized financial advice.

    14. Do NOT force a directional opinion when the evidence is
        genuinely mixed. In that situation, use NEUTRAL.

    Confidence should represent your confidence in the analytical
    assessment, NOT the probability that the stock will rise or
    fall.

        IMPORTANT INTERPRETATION RULES:

    - Do not classify an event as positive or negative merely
    because it occurred.

    - Preserve the interpretation from the research report.
    If the report explicitly identifies an event as neutral,
    do not reclassify it as negative without evidence.

    - Do not describe a financial metric as "strong", "weak",
    "healthy", or "poor" unless the supplied report provides
    a basis for that interpretation, such as historical or
    peer comparison.

    - Do not infer long-term business performance from a
    short-term stock price movement.

    - Do not treat an analyst rating or price target as an
    objective assessment of the company's value.

    - If the available information is mixed or insufficient,
    NEUTRAL is a valid and preferred conclusion.

    - The perspective should synthesize the report rather than
    introduce new analysis that requires information absent
    from the report.

    - When evaluating analyst opinions, consider the complete
      rating and target change together.

    - Do not classify a price-target increase as independently
    bullish when the analyst's underlying rating remains Neutral.

    - Do not count the same analyst update as both a positive and
    neutral signal.

    Return ONLY the structured perspective.
    """

    try:
        result = structured_llm.invoke(prompt)

        return {
            "perspective": result
        }
    except Exception as e:
        return {
            "errors": [f"Perspective generation failed: {str(e)}"]
        }