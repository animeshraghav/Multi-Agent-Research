import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily and return the top search results.
    """
    results = tavily.search(
        query=query,
        max_results=5
    )
    out = []
    for r in results["results"]:
        out.append(
            f"""Title: {r['title']}
URL: {r['url']}
Content: {r['content']}
"""
        )

    return "\n\n".join(out)