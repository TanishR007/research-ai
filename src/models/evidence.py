from enum import Enum
from pydantic import BaseModel, Field


class ClaimType(str, Enum):
    MARKET = "market"
    NEWS = "news"
    FUNDAMENTAL = "fundamental"
    ANALYST = "analyst"


class Claim(BaseModel):
    statement: str
    claim_type: ClaimType
    source_urls: list[str] = Field(default_factory=list)


class ClaimList(BaseModel):
    claims: list[Claim] = Field(default_factory=list)
