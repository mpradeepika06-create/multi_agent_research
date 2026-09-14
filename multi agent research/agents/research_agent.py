from tools.web_search import search_web, scrape_page


class ResearchAgent:

    def __init__(self, max_sources=10):
        self.max_sources = max_sources

    def research(self, topic, progress_callback=None):

        if progress_callback:
            progress_callback(
                "🔎 Research Agent: searching the web..."
            )

        queries = [
            f"{topic} overview research",
            f"{topic} latest developments",
            f"{topic} benefits advantages",
            f"{topic} risks disadvantages",
            f"{topic} statistics facts",
            f"{topic} applications real world",
        ]

        all_results = []

        for query in queries:

            results = search_web(
                query,
                max_results=5
            )

            all_results.extend(results)

        # Remove duplicate URLs
        unique_results = []

        seen_urls = set()

        for result in all_results:

            url = result.get("url", "")

            if url and url not in seen_urls:

                seen_urls.add(url)
                unique_results.append(result)

        unique_results = unique_results[:self.max_sources]

        # Extract webpage content
        sources = []

        for i, result in enumerate(unique_results, start=1):

            if progress_callback:
                progress_callback(
                    f"🌐 Research Agent: reading source {i}/{len(unique_results)}"
                )

            content = scrape_page(
                result["url"]
            )

            sources.append({
                "id": i,
                "title": result["title"],
                "url": result["url"],
                "snippet": result["snippet"],
                "content": content
            })

        if progress_callback:
            progress_callback(
                f"✅ Research Agent: collected {len(sources)} sources"
            )

        return sources