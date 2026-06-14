from app.code_ingestion.code_chunker import (
    CodeChunker,
)
from app.code_ingestion.repository_scanner import (
    RepositoryScanner,
)
from app.schemas.code_chunk import (
    CodeChunk,
)
from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)


class CodeIngestionService:
    def __init__(
        self,
        scanner: RepositoryScanner,
        chunker: CodeChunker,
        retrieval_service: (
            CodeRetrievalService
        ),
    ) -> None:
        self.scanner = scanner

        self.chunker = chunker

        self.retrieval_service = (
            retrieval_service
        )

    async def ingest_repository(
        self,
        repo_path: str,
    ) -> list[CodeChunk]:
        files = self.scanner.scan(
            repo_path
        )

        all_chunks = []

        for file in files:
            chunks = (
                self.chunker.chunk_file(
                    file
                )
            )

            all_chunks.extend(chunks)

        await self.retrieval_service.index_chunks(
            all_chunks
        )

        return all_chunks