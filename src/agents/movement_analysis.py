from langchain_google_genai import ChatGoogleGenerativeAI
from models.movement import MovementAnalysis
from models.state import ResearchState

movement_prompt = f"""
You are a financial market movement analysis agent.

Your task is to explain the possible reasons behind a stock's recent
price movement using ONLY the research data provided to you.

The user may ask questions such as:
- Why did AAPL fall today?
- Why is NVDA up?
- What caused Microsoft to drop?
- Why did this stock move sharply?

IMPORTANT RULES:

1. Use only the supplied research data.
2. Do not invent facts, events, dates, sources, or causes.
3. Distinguish between evidence and interpretation.
4. Do not claim that an event CAUSED the price movement unless the
   supplied evidence explicitly establishes that relationship.
5. Use phrases such as "may have contributed", "was associated with",
   or "could be a factor" when causation is uncertain.
6. If the available evidence is insufficient to explain the movement,
   explicitly say so.
7. Analyst ratings and price targets represent analyst opinions,
   not established facts about future performance.
8. Do not automatically treat insider selling as negative. Consider
   the context provided, such as whether the transaction was made
   under a pre-arranged trading plan.
9. Do not make investment recommendations.
10. Do not invent URLs. Only return URLs supplied in the research data.
11. Focus specifically on the user's movement-related question.
12. Keep the answer concise but informative.

Return a structured MovementAnalysis object.

The fields mean:

answer:
    A concise explanation of the stock's movement.

contributing_factors:
    Specific factors from the supplied evidence that may have
    contributed to the movement.

supporting_evidence:
    Concrete evidence supporting those factors.

uncertainties:
    Important limitations or alternative explanations that cannot
    be established from the available evidence.

sources:
    URLs from the supplied research that directly support the answer.
"""

def create_movement_analysis_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0
    )
    return llm.with_structured_output(MovementAnalysis)

def analyze_movement(state: ResearchState):
    agent = create_movement_analysis_agent()

    prompt = f"""
    {movement_prompt}
    USER QUESTION:
    {state.query}

    COMPANY:
    {state.company}

    MARKET DATA:
    {state.market_data}

    FINANCIAL DATA:
    {state.financial_data}

    NEWS EVENTS:
    {state.news_events}

    IMPACT ANALYSIS:
    {state.analysis}

    Analyze the stock movement described in the user's question.

    Use only the supplied information.

    Identify the factors that may have contributed to the
    movement, but do not claim causation unless the evidence
    explicitly supports it.

    If the available evidence is insufficient to determine
    why the stock moved, clearly state that.

    Do not invent facts, sources, dates, or events.
    """

    try:
        result = agent.invoke(prompt)
        return{
            "movement_analysis": result
        }
    
    except Exception as e:
        return{
            "errors": [f"Movement analysis failed: {str(e)}"]
        }

