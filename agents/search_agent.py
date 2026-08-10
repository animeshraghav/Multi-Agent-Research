from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from tools.search_tools import web_search

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.google_api_key,
    temperature=settings.temperature,
)

search_agent = create_react_agent(
    model=llm,
    tools=[web_search],
     prompt="""
You are a web research assistant.

Always use the web_search tool.

Never answer from your own knowledge.

Return the tool output.
"""
)