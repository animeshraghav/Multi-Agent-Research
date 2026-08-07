from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.scraper_tool import scrape_url

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",

)

reader_agent = create_react_agent(
    model=llm,
    tools=[scrape_url],
)