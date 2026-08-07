import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool


@tool
def scrape_url(url: str) -> str:
    """
    Scrape the readable text from a webpage.
    """
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )
        for tag in soup(
            [
                "script",
                "style",
                "header",
                "footer",
                "nav",
                "noscript",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True,
        )
        return text[:5000]

    except Exception as e:
        return f"Scraping failed: {e}"