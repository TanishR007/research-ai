from models.analysis import NewsEvent, NewsEventsList
from models.state import ResearchState
from llm.client import llm

structured_llm = llm.with_structured_output(NewsEventsList)

def extract_news_events(state: ResearchState) -> dict:
    if state.news is None:
        return {
            "errors": ["cannot extract events: news data unavailable"]
        }
    if not state.news.articles:
        return {
            "news_events": [] 
        } 
    news_context=[]
    for article in state.news.articles:
        news_context.append(
            {
                "title": article.title,
                "content": article.content,
                "published_at": (
                    article.published_at.isoformat()
                    if article.published_at
                    else None
                ),
                "source": article.source,
                "url": article.url,
            }
        )
    
    prompt = f"""
    You are a financial news event extraction agent.

Company:
{state.company.company_name if state.company else "Unknown"}

Ticker:
{state.company.ticker if state.company else "Unknown"}

USER QUERY:
{state.query}

NEWS ARTICLES:
{news_context}

Your task is to extract concrete events explicitly reported
in the supplied news articles.

Rules:

1. Use ONLY information present in the supplied articles.
2. Do not invent facts.
3. Do not infer causes or consequences.
4. Do not determine whether an event is positive or negative.
5. Do not predict stock movements.
6. Do not add financial interpretations.
7. Ignore articles that do not contain a meaningful concrete event.
8. Multiple articles reporting the same event should produce one event.
9. Preserve the source URL and publication date for every event.
10. Prefer specific events over vague statements.
11. Prioritize events that are temporally relevant to the user's query.
12. For questions about recent or current stock movement, prioritize
    events from the current trading session and the most recent few
    trading sessions.
13. Do not extract every historical event listed in an article.
14. Include older events only when they provide meaningful context
    for the user's question.

Examples of valid events:

- Company announced quarterly earnings.
- Executive sold shares.
- Company launched a new product.
- Company received regulatory approval.
- Analyst changed a price target.
- Company announced an acquisition.

Examples of invalid events:

- Company is a good investment.
- Stock looks overvalued.
- Investors are optimistic.
- The stock may rise.
- Strong fundamentals.

Return only the extracted structured events.
"""
    try:
        events = structured_llm.invoke(prompt)

        return {
            "news_events": events.events
        }
    except Exception as e:
        return {
            "errors": [f"Event extraction failed: {str(e)}"]
        }