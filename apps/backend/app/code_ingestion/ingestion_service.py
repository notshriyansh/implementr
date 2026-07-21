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

        self.repository_analyzer = (
        repository_analyzer
    )

    async def ingest_repository(
        self,
        repo_path: str,
    ) -> int:
        
        self.repository_analyzer.analyze(
            repo_path
        )

        files = self.scanner.scan(
            repo_path
        )

        total_chunks = 0


        for file in files:
            chunks = self.chunker.chunk_file(file)

            if chunks:

                total_chunks += len(
                    chunks
                )

                await self.retrieval_service.index_chunks(
                    chunks
                )

            symbols = self.symbol_extractor.extract_symbols(str(file))

            if symbols:
                await self.symbol_retrieval_service.index_symbols(symbols)

            for symbol in symbols:

                concepts = self.concept_service.symbol_to_concepts(symbol)

                for concept in concepts:
                    self.concept_index.add(concept)

            del chunks
            del symbols

        return total_chunks
