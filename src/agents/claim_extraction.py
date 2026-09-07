from models.evidence import ClaimList
from models.state import ResearchState
from llm.client import llm


structured_llm = llm.with_structured_output(ClaimList)


def extract_claims(state: ResearchState) -> dict:
    """
    Extract important factual claims from the research state
    using an LLM with structured output.
    """

    if state.company is None:
        return {
            "errors": [
                "Cannot extract claims: company not resolved"
            ]
        }

    if state.analysis is None:
        return {
            "errors": [
                "Cannot extract claims: analysis unavailable"
            ]
        }

    prompt = f"""
You are a financial research claim extraction agent.

Your purpose is to extract important factual claims from
the supplied research information so that they can later
be independently verified.

Company:
{state.company}

MARKET DATA:
{state.market_data}

FUNDAMENTAL DATA:
{state.financial_data}

NEWS EVENTS:
{state.news_events}

IMPACT ANALYSIS:
{state.analysis}

Inspect ALL supplied information sources independently:

- MARKET DATA
- FUNDAMENTAL DATA
- NEWS EVENTS
- IMPACT ANALYSIS

Do not summarize only the Impact Analysis.

Extract important factual claims from every applicable
category.

Do not stop after extracting one claim.

Coverage is more important than extreme compression.

For the market data, extract the important market movement,
but do NOT describe a value as a "closing price" unless the
supplied data explicitly identifies it as a closing price.

Do NOT infer a date for market data from the current date,
news publication date, or any other source.

Use only dates explicitly associated with the underlying fact.

Classification:

MARKET:
Only price, price change, percentage change, volume, currency,
or other trading information.

FUNDAMENTAL:
Only financial or valuation metrics.

NEWS:
Concrete company events, transactions, announcements,
executive actions, filings, or other factual company events.

ANALYST:
Analyst ratings, recommendations, upgrades, downgrades,
reiterations, or price targets.

Do NOT use MARKET as a default category.

Source rules:

- For claims derived from NEWS EVENTS, include the source_url
  from the corresponding news event in source_urls.
- For claims derived from MARKET DATA or FUNDAMENTAL DATA,
  leave source_urls empty unless an explicit source URL is
  provided in the supplied data.
- Do not invent URLs.
- Do not use URLs that were not supplied in the input.

Claim rules:

1. Claims must be factual and independently verifiable.
2. Do not create claims that are merely opinions or conclusions.
3. Do not turn the impact analysis into new factual claims
   unless the underlying fact is explicitly present in the
   supplied information.
4. Do not infer causation.
5. Do not invent dates, numbers, sources, or events.
6. Do not combine unrelated facts into a single claim.
7. Prefer specific claims over vague summaries.
8. Avoid duplicate claims.
9. Extract claims that are useful for downstream verification.
10. Do not manufacture claims merely to reach a target count.

For a typical research request, aim for approximately
5–10 high-value claims when the supplied information
supports them.

Return ONLY the structured claims.
"""

    try:
        result = structured_llm.invoke(prompt)

        return {
            "claims": result.claims
        }

    except Exception as e:
        return {
            "errors": [
                f"Claim extraction failed: {str(e)}"
            ]
        }