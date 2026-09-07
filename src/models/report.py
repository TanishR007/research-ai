from enum import Enum
from pydantic import BaseModel, Field


class InvestmentView(str, Enum):
    BULLISH = "bullish"
    CAUTIOUSLY_BULLISH = "cautiously_bullish"
    NEUTRAL = "neutral"
    CAUTIOUSLY_BEARISH = "cautiously_bearish"
    BEARISH = "bearish"


class ResearchReport(BaseModel):
    executive_summary: str

    market_snapshot: str

    recent_developments: list[str] = Field(
        default_factory=list
    )

    positive_factors: list[str] = Field(
        default_factory=list
    )

    negative_factors: list[str] = Field(
        default_factory=list
    )

    uncertainties: list[str] = Field(
        default_factory=list
    )

    key_claims: list[str] = Field(
        default_factory=list
    )

    sources: list[str] = Field(
        default_factory=list
    )


class StockPerspective(BaseModel):
    overall_view: InvestmentView

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    reasoning: str

    positive_factors: list[str] = Field(
        default_factory=list
    )

    negative_factors: list[str] = Field(
        default_factory=list
    )

    key_risks: list[str] = Field(
        default_factory=list
    )

    key_uncertainties: list[str] = Field(
        default_factory=list
    )

    catalysts_to_watch: list[str] = Field(
        default_factory=list
    )