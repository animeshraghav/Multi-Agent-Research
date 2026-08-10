from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from tools.scraper_tool import scrape_url

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.google_api_key,
    temperature=settings.temperature,
)

reader_agent = create_react_agent(
    model=llm,
    tools=[scrape_url],
)