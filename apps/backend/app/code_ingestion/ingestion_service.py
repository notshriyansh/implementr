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
from app.code_ingestion.symbol_extractor import (
    SymbolExtractor,
)
from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)
from app.schemas.code_symbol import (
    CodeSymbol,
)


class CodeIngestionService:
    def __init__(
        self,
        scanner: RepositoryScanner,
        chunker: CodeChunker,
        retrieval_service: (
            CodeRetrievalService
        ),
        symbol_extractor: (
            SymbolExtractor
        ),
        symbol_retrieval_service: (
            SymbolRetrievalService
        ),
    ) -> None:
        self.scanner = scanner

        self.chunker = chunker

        self.retrieval_service = (
            retrieval_service
        )

        self.symbol_extractor = (
            symbol_extractor
        )

        self.symbol_retrieval_service = (
            symbol_retrieval_service
        )

    async def ingest_repository(
        self,
        repo_path: str,
    ) -> list[CodeChunk]:
        files = self.scanner.scan(
            repo_path
        )

        all_chunks: list[
            CodeChunk
        ] = []

        all_symbols: list[
            CodeSymbol
        ] = []

        for file in files:
            chunks = (
                self.chunker.chunk_file(
                    file
                )
            )

            all_chunks.extend(
                chunks
            )

            symbols = (
                self.symbol_extractor
                .extract_symbols(file)
            )

            all_symbols.extend(
                symbols
            )

        await (
            self.retrieval_service
            .index_chunks(
                all_chunks
            )
        )

        await (
            self.symbol_retrieval_service
            .index_symbols(
                all_symbols
            )
        )

        return all_chunks