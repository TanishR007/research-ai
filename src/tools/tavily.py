from tavily import TavilyClient
from config.settings import settings

class TavilyAPI:
    def __init__(self):
        self.client = TavilyClient(api_key=settings.tavily_api_key)

    def search_news(self, query):
        response = self.client.search(
            query=query,
            topic="news",
            search_depth="advanced",
            max_results=10,
        )
        return response