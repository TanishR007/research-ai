from models.company import CompanyIdentity, AssetType
from models.state import ResearchState
from tools.market_api import MarketAPI


market_api = MarketAPI()


def resolve_ticker(state: ResearchState) -> dict:
    query = state.query.strip()

    if not query:
        return {
            "errors": ["Ticker/company query cannot be empty"]
        }

    try:
        results = market_api.search_symbol(query)

        if not results:
            return {
                "errors": [
                    f"Unable to resolve company: {query}"
                ]
            }

        normalized_query = query.upper()

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