from app.code_ingestion.code_chunker import (
    CodeChunker,
)
from app.code_ingestion.repository_scanner import (
    RepositoryScanner,
)
from app.schemas.code_chunk import (
    CodeChunk,
)


class CodeIngestionService:
    def __init__(
        self,
        scanner: RepositoryScanner,
        chunker: CodeChunker,
    ) -> None:
        self.scanner = scanner

        self.chunker = chunker

    def ingest_repository(
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

        return all_chunks