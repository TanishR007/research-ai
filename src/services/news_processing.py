from datetime import datetime, timedelta, timezone
from models.news import NewsArticle

def deduplicate_articles(articles: list[NewsArticle]) -> list[NewsArticle]:
    seen_urls = set()
    unique_articles = []
    for article in articles:
        normalized_url = article.url.rstrip("/")

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_articles.append(article)
    return unique_articles

def filter_recent_articles(articles: list[NewsArticle], days: int = 7) -> list[NewsArticle]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    return [article for article in articles if article.published_at is None or article.published_at >= cutoff]

def filter_relevant_article(articles: list[NewsArticle], minScore: float = 0.65) -> list[NewsArticle]:
    return [article for article in articles if article.relevance_score is None or article.relevance_score >= minScore]

def process_news(articles: list[NewsArticle], days: int = 7, minScore: float = 0.65) -> list[NewsArticle]:
    articles = deduplicate_articles(articles)
    articles = filter_recent_articles(articles, days)
    articles = filter_relevant_article(articles, minScore)
    return articles