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
from app.concepts.concept_service import (
    ConceptService,
)
from app.concepts.concept_index import (
    ConceptIndex,
)
from app.code_ingestion.repository_analyzer import (
    RepositoryAnalyzer,
)
from app.repository_sources.repository_registry import RepositoryRegistry
from app.schemas.code_symbol import (
    CodeSymbol,
)
from app.repository_sources.factory import (
    RepositorySourceFactory,
)
from app.schemas.concept import Concept


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
        repository_registry: RepositoryRegistry,
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

        self.concept_service = (
            concept_service
        )

        self.concept_index = (
            concept_index
        )

        self.repository_info = None

        self.repository_registry = repository_registry

        self.repository_analyzer = (
        repository_analyzer
    )

    async def ingest_repository(
        self,
        location: str,
    ) -> list[CodeChunk]:

        source = RepositorySourceFactory.create(
            location
        )

        repository = await source.prepare(
            location
        )

        self.repository_info = repository

        self.repository_analyzer.analyze(
            repo_path=str(repository.repository_root),
            repository_id=repository.repository_id,
        )

        files = self.scanner.scan(
            str(repository.repository_root)
        )

        all_chunks: list[
            CodeChunk
        ] = []

        all_symbols: list[
            CodeSymbol
        ] = []

        all_concepts: list[Concept] = []

        for file in files:

            chunks = self.chunker.chunk_file(
                file_path=file,
                repository_root=repository.repository_root,
                repository_name=repository.repository_name,
                repository_id=repository.repository_id,
            )

            all_chunks.extend(
                chunks
            )

            symbols = (
                self.symbol_extractor.extract_symbols(
                    file_path=str(file),
                    repository_root=repository.repository_root,
                    repository_name=repository.repository_name,
                    repository_id=repository.repository_id,
                )
            )

            all_symbols.extend(
                symbols
            )

            for symbol in symbols:
                all_concepts.extend(
                    self.concept_service.symbol_to_concepts(
                        symbol
                    )
                )

        await self.retrieval_service.replace_repository_chunks(
            repository.repository_id,
            all_chunks,
        )

        await self.symbol_retrieval_service.replace_repository_symbols(
            repository.repository_id,
            all_symbols,
        )

        self.concept_index.replace_repository(
            repository.repository_id,
            all_concepts,
        )

        self.repository_registry.register(repository)

        return all_chunks
