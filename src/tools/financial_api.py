import finnhub
from config.settings import settings

class FinancialAPI:
    def __init__(self):
        self.client = finnhub.Client(api_key=settings.finnhub_api_key)
    
    def get_basic_financials(self, ticker: str):
        return self.client.company_basic_financials(
            ticker,
            "all",
        )