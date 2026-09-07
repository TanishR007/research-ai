from pydantic import BaseModel
from enum import Enum;
class AssetType(str, Enum):
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    MUTUAL_FUND = "mutual_fund"
    CRYPTO = "crypto"
    FOREIGN_EXCHANGE = "forex"

class CompanyIdentity(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    country: str
    asset_type: AssetType