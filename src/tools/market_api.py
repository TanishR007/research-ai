from twelvedata import TDClient
from config.settings import settings

class MarketAPI:
    def __init__(self):
        self.client = TDClient(apikey=settings.twelve_data_api_key)
    
    def get_quote(self, ticker):
        quote = self.client.quote(symbol=ticker)
        return quote.as_json()

    def search_symbol(self, query: str):
        result = self.client.symbol_search(symbol=query)
        return result.as_json()