from models.state import ResearchState
from models.market import MarketData
from tools.market_api import MarketAPI

market_api = MarketAPI();

def get_market_data(state: ResearchState) -> dict:

    if state.company is None:
        return{
            "errors": ["Cannot retrieve market data: company not resolved"]
        }
    
    ticker = state.company.ticker

    try:
        data =market_api.get_quote(ticker)
        
        market_data = MarketData(
            ticker=ticker,
            price=float(data["close"]),
            change=float(data["change"]) if data.get("change") else None,
            percent_change=float(data["percent_change"]) if data.get("percent_change") else None,
            volume=int(data["volume"]) if data.get("volume") else None,
            currency=data.get("currency"),
            timestamp=data.get("timestamp")
        )
        return {
            "market_data": market_data
        }
    except Exception as e:
        return {
            "errors": [f"Error getting market data: {str(e)}"]
        }