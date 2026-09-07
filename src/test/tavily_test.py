from agents.news import get_news
from models.company import CompanyIdentity, AssetType
from models.state import ResearchState


state = ResearchState(
    query="apple",
    company=CompanyIdentity(
        ticker="AAPL",
        company_name="Apple Inc.",
        exchange="NASDAQ",
        country="United States",
        asset_type=AssetType.STOCK,
    )
)

response = get_news(state)

print(response)

for article in response["news"].articles:
    print(article.title)
    print(article.source)
    print(article.published_at)
    print(article.relevance_score)
    print("---")