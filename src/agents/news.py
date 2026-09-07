from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse
from models.news import NewsData, NewsArticle
from models.state import ResearchState 
from tools.tavily import TavilyAPI
from services.news_processing import process_news

tavily_api = TavilyAPI()

def parse_published_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value)
    except Exception as e:
        return None

def get_news(state: ResearchState) -> dict:
    if state.company is None:
        return{
            "errors": ["Cannot retrieve news: company not resolved"]
        }
    
    company = state.company
    query = f"{company.company_name} {company.ticker} latest news"

    try:
        results = tavily_api.search_news(query=query)
        articles = []

        for result in results.get("results", []):
            url = result.get("url")
            if not url:
                continue
            source = urlparse(url).netloc
            article = NewsArticle(
                title=result.get("title", ""),
                url=url,
                content=result.get("content"),
                published_at=parse_published_date(result.get("published_date")),
                source=source,
                relevance_score=result.get("score"),
            )
            articles.append(article)
        articles = process_news(articles)
        return {
            "news": NewsData(articles=articles)
        }
    except Exception as e:
        return {
            "errors": [f"News retrieval failed: {str(e)}"]
        }