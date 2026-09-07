from pydantic import BaseModel

class MarketData(BaseModel):
    ticker: str
    price: float
    change: float | None=None
    percent_change: float | None=None
    volume: int | None=None
    currency: str | None=None
    timestamp: int | None=None
