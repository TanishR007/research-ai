from datetime import date
from pydantic import BaseModel

class FinancialData(BaseModel):
    ticker: str
    market_cap: float | None = None
    pe_ratio: float | None = None
    pb_ratio: float | None = None
    net_margin: float | None = None
    operating_margin: float | None = None
    debt_to_equity: float | None = None
    latest_period: date | None = None
