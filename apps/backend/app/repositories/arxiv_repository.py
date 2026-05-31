import feedparser
import httpx

from app.schemas.paper import Paper, PaperAuthor

class ArxivRepository:
    BASE_URL = "http://export.arxiv.org/api/query"

    async def search_papers(
            self,
            query: str,
            max_results: int = 5,
    ) -> list[Paper]:
        search_query = query.replace(" ", "+")

        url = (
            f"{self.BASE_URL}"
            f"?search_query=all:{search_query}"
            f"&start=0"
            f"&max_results={max_results}"
        )

        async with httpx.AsyncClient(
            follow_redirects=True,
        ) as client:
            response = await client.get(url)

        response.raise_for_status()

        feed = feedparser.parse(response.text)

        papers: list[Paper] =  []

        for entry in feed.entries:
            authors = [
                PaperAuthor(name=author.name)
                for author in entry.authors
            ]

            paper = Paper(
                title=entry.title,
                summary=entry.summary,
                pdf_url=entry.id.replace(
                    "/abs/",
                    "/pdf/",
                )
                + ".pdf",
                published=entry.published,
                authors=authors,
            )

            papers.append(paper)

        return papers
