from tavily import TavilyClient
from langchain_core.tools import tool
from config import settings


# ============================================================
# TAVILY CLIENT
# ============================================================

tavily = TavilyClient(
    api_key=settings.tavily_api_key
)


# ============================================================
# WEB SEARCH TOOL
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily and return the most relevant
    search results with titles, URLs, and content snippets.
    """

    results = tavily.search(
        query=query,
        max_results= settings.tavily_max_results
    )

    output = []

    for result in results.get("results", []):
        output.append(
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'N/A')}"
        )

    return "\n\n---\n\n".join(output)