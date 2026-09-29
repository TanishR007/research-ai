from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from models.company import CompanyIdentity, AssetType
from models.state import ResearchState
from tools.market_api import MarketAPI


market_api = MarketAPI()


class TickerExtraction(BaseModel):
    company_query: str


def create_ticker_extractor():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0,
    )

    return llm.with_structured_output(TickerExtraction)


def resolve_ticker(state: ResearchState) -> dict:
    query = state.query.strip()

    if not query:
        return {
            "errors": ["Ticker/company query cannot be empty"]
        }

    try:
        extractor = create_ticker_extractor()

        extraction_prompt = f"""
        Extract the company or stock ticker that the user is asking
        about.

        USER QUERY:
        {query}

        Examples:

        "Why did NVDA fall today?"
        -> NVDA

        "Why is Apple down?"
        -> Apple

        "Why did Microsoft stock jump?"
        -> Microsoft

        "Give me a research report on AAPL"
        -> AAPL

        "What is happening with Nvidia?"
        -> Nvidia

        Return only the company or ticker that should be searched
        in a financial market symbol database.

        Do not answer the user's question.
        Do not provide an explanation.
        """

        extraction = extractor.invoke(extraction_prompt)

        company_query = extraction.company_query.strip()

        if not company_query:
            return {
                "errors": [
                    f"Unable to extract company from query: {query}"
                ]
            }


        results = market_api.search_symbol(company_query)

        if not results:
            return {
                "errors": [
                    f"Unable to resolve company: {company_query}"
                ]
            }

        normalized_query = company_query.upper()

        exact_matches = [
            result
            for result in results
            if result.get("symbol", "").upper() == normalized_query
        ]

        candidates = exact_matches if exact_matches else results

        stock_candidates = [
            result
            for result in candidates
            if result.get("instrument_type", "").lower()
            in {"common stock", "stock", "equity"}
        ]

        if stock_candidates:
            candidates = stock_candidates

        us_candidates = [
            result
            for result in candidates
            if result.get("country", "").lower()
            in {"united states", "usa", "us"}
        ]

        if us_candidates:
            candidates = us_candidates

        # ---------------------------------------------------------
        # Step 5: Build CompanyIdentity
        # ---------------------------------------------------------

        candidate = candidates[0]

        company = CompanyIdentity(
            ticker=candidate["symbol"],
            company_name=candidate["instrument_name"],
            exchange=candidate["exchange"],
            country=candidate["country"],
            asset_type=AssetType.STOCK,
        )

        return {
            "company": company
        }

    except Exception as e:
        return {
            "errors": [
                f"Ticker resolution failed: {str(e)}"
            ]
        }