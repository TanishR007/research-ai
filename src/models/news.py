from pydantic import BaseModel, Field
from datetime import datetime

class NewsArticle(BaseModel):
    title: str
    url: str
    content: str | None = None
    published_at: datetime | None = None
    source: str | None = None
    relevance_score: float | None = None

class NewsData(BaseModel):
    articles: list[NewsArticle] = Field(default_factory=list)