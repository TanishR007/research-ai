import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "research-ai"
    development: bool = "true"
    twelve_data_api_key: str | None = None
    tavily_api_key: str | None = None
    finnhub_api_key: str| None = None
    gemini_api_key: str | None = None
    langsmith_api_key: str | None = None
    langsmith_tracing: bool = True
    langsmith_project: str = "stock-intelligence-ai"
    langsmith_endpoint: str = "https://api.smith.langchain.com"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()