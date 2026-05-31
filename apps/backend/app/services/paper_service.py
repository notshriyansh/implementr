from app.repositories.arxiv_repository import ArxivRepository
from app.schemas.paper import Paper

class PaperService:
    def __init__(
            self,
            arxiv_repository: ArxivRepository,
    ) -> None:
        self.arxiv_repository = arxiv_repository

    async def search_papers(
            self,
            query: str,
    ) -> list[Paper]:
        return await self.arxiv_repository.search_papers(
            query=query,
        )