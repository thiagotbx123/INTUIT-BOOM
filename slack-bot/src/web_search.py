"""
Web Search Module
Searches the web for QuickBooks/Intuit related information.
Uses DuckDuckGo (no API key needed) or Google Custom Search.
"""

import requests
from typing import List, Dict
from urllib.parse import quote_plus


class WebSearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using DuckDuckGo Instant Answer API."""
        # Add QuickBooks context to query
        enhanced_query = f"QuickBooks Online {query}"

        url = f"https://api.duckduckgo.com/?q={quote_plus(enhanced_query)}&format=json&no_html=1"

        try:
            response = self.session.get(url, timeout=10)
            data = response.json()

            results = []

            # Abstract (main result)
            if data.get("Abstract"):
                results.append(
                    {
                        "title": data.get("Heading", "Result"),
                        "snippet": data.get("Abstract"),
                        "url": data.get("AbstractURL", ""),
                        "source": data.get("AbstractSource", "DuckDuckGo"),
                    }
                )

            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append(
                        {
                            "title": topic.get("Text", "")[:100],
                            "snippet": topic.get("Text", ""),
                            "url": topic.get("FirstURL", ""),
                            "source": "DuckDuckGo Related",
                        }
                    )

            return results[:max_results]

        except Exception as e:
            return [{"error": str(e)}]

    def search_intuit_help(self, query: str) -> List[Dict]:
        """Search Intuit's help documentation directly."""
        # This would scrape or use Intuit's search
        # For now, returns formatted search suggestion
        search_url = f"https://quickbooks.intuit.com/learn-support/en-us/search?q={quote_plus(query)}"

        return [
            {
                "title": "Intuit Help Center Search",
                "snippet": f"Search Intuit Help for: {query}",
                "url": search_url,
                "source": "Intuit Help",
            }
        ]

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Combined search across sources."""
        results = []

        # DuckDuckGo results
        ddg_results = self.search_duckduckgo(query, max_results)
        results.extend(ddg_results)

        # Intuit help link
        intuit_results = self.search_intuit_help(query)
        results.extend(intuit_results)

        return results

    def get_web_context(self, query: str) -> str:
        """Get formatted web search results for context."""
        results = self.search(query)

        if not results or (len(results) == 1 and "error" in results[0]):
            return "Web search returned no results or failed."

        summary_parts = ["## Web Search Results\n"]

        for result in results:
            if "error" in result:
                continue
            summary_parts.append(f"### {result.get('title', 'Result')}")
            summary_parts.append(f"Source: {result.get('source', 'Unknown')}")
            summary_parts.append(f"URL: {result.get('url', 'N/A')}")
            summary_parts.append(f"{result.get('snippet', '')[:300]}")
            summary_parts.append("")

        return "\n".join(summary_parts)


# Singleton
_web_search = None


def get_web_searcher() -> WebSearch:
    global _web_search
    if _web_search is None:
        _web_search = WebSearch()
    return _web_search
