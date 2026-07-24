from app.code_ingestion.code_chunker import (
    CodeChunker,
)
from app.code_ingestion.repository_scanner import (
    RepositoryScanner,
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
from app.concepts.concept_service import (
    ConceptService,
)
from app.concepts.concept_index import (
    ConceptIndex,
)
from app.code_ingestion.repository_analyzer import (
    RepositoryAnalyzer,
)
from app.schemas.code_chunk import (
    CodeChunk,
)
from app.schemas.code_symbol import (
    CodeSymbol,
)
from app.sources.base import BaseRepositorySource


class CodeIngestionService:
    def __init__(
        self,
        scanner: RepositoryScanner,
        chunker: CodeChunker,
        retrieval_service: CodeRetrievalService,
        symbol_extractor: SymbolExtractor,
        symbol_retrieval_service: SymbolRetrievalService,
        concept_service: ConceptService,
        concept_index: ConceptIndex,
        repository_analyzer: RepositoryAnalyzer,
    ) -> None:
        self.scanner = scanner
        self.chunker = chunker
        self.retrieval_service = retrieval_service
        self.symbol_extractor = symbol_extractor
        self.symbol_retrieval_service = symbol_retrieval_service
        self.concept_service = concept_service
        self.concept_index = concept_index
        self.repository_analyzer = repository_analyzer

    async def ingest_repository(
        self,
        source: BaseRepositorySource,
    ) -> int:

        repository_root = await source.prepare()

        self.repository_analyzer.analyze(
            repository_root
        )

        files = self.scanner.scan(
            repository_root
        )

        total_chunks = 0

        all_chunks: list[CodeChunk] = []
        all_symbols: list[CodeSymbol] = []

        for file in files:

            chunks = self.chunker.chunk_file(
                repository_root,
                file,
            )

            if chunks:
                total_chunks += len(chunks)
                all_chunks.extend(chunks)

            symbols = self.symbol_extractor.extract_symbols(
                repository_root,
                file,
            )

            if symbols:
                all_symbols.extend(symbols)

                for symbol in symbols:
                    concepts = self.concept_service.symbol_to_concepts(
                        symbol
                    )

                    for concept in concepts:
                        self.concept_index.add(concept)

        if all_chunks:
            await self.retrieval_service.index_chunks(
                all_chunks
            )

        if all_symbols:
            await self.symbol_retrieval_service.index_symbols(
                all_symbols
            )

        return total_chunks