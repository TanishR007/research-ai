from pydantic import BaseModel, Field
from datetime import datetime

class NewsEvent(BaseModel):
    title: str
    description: str
    source_url: str
    published_at: datetime | None=None

class ImpactAnalysis(BaseModel):
    summary: str
    positive_factors: list[str] = Field(default_factory=list)
    negative_factors: list[str] = Field(default_factory=list)
    neutral_factors: list[str] = Field(default_factory=list)

class NewsEventsList(BaseModel):
    events: list[NewsEvent] = Field(default_factory=list)