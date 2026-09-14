import requests
from bs4 import BeautifulSoup
from ddgs import DDGS


def search_web(query, max_results=8):
    """
    Search the web using DuckDuckGo.
    Returns a list of search results.
    """

    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        output = []

        for result in results:
            output.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

        return output

    except Exception as e:
        return [{
            "title": "Search Error",
            "url": "",
            "snippet": str(e)
        }]


def scrape_page(url, max_chars=10000):
    """
    Extract readable text from a webpage.
    """

    if not url:
        return ""

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:max_chars]

    except Exception:
        return ""