from tools.financial_api import FinancialAPI

api = FinancialAPI()
print(api.get_basic_financials("AAPL"))
