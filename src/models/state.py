from pydantic import BaseModel, Field
from typing import Annotated
from operator import add
from models.market import MarketData
from models.company import CompanyIdentity
from models.news import NewsData
from models.financials import FinancialData
from models.analysis import ImpactAnalysis, NewsEvent
from models.evidence import Claim
from models.report import ResearchReport, StockPerspective
from models.movement import MovementAnalysis

class ResearchState(BaseModel):
    query: str
    company: CompanyIdentity | None = None
    market_data: MarketData | None=None
    news: NewsData | None = None
    news_events: list[NewsEvent] = Field(default_factory=list)
    financial_data: FinancialData | None = None
    analysis: ImpactAnalysis | None = None
    movement_analysis: MovementAnalysis | None = None
    claims: list[Claim] = Field(default_factory=list)
    report: ResearchReport | None = None
    perspective: StockPerspective | None = None
    errors: Annotated[list[str], add] = Field(default_factory=list)
