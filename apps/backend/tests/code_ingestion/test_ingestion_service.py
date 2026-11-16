
from pathlib import Path

import asyncio

from app.code_ingestion.ingestion_service import CodeIngestionService
from app.concepts.concept_index import ConceptIndex
from app.concepts.concept_service import ConceptService
from app.repository_sources.repository_info import RepositoryInfo
from app.repository_sources.repository_registry import RepositoryRegistry
from app.schemas.code_chunk import CodeChunk
from app.schemas.code_symbol import CodeSymbol
from app.schemas.concept import Concept


REPOSITORY_ID = "repo-a"
OTHER_REPOSITORY_ID = "repo-b"


class FakeSource:
    def __init__(self, repository):
        self.repository = repository

    async def prepare(self, location):
        return self.repository


class FakeScanner:
    def __init__(self):
        self.files = []

    def scan(self, repo_path):
        return list(self.files)


class FakeChunker:
    def __init__(self):
        self.chunks = []

    def chunk_file(self, **kwargs):
        return list(self.chunks)


class FakeSymbolExtractor:
    def __init__(self):
        self.symbols = []

    def extract_symbols(self, **kwargs):
        return list(self.symbols)


class FakeRetrievalService:
    def __init__(self):
        self.chunks = []
        self.replacement_calls = []

    async def replace_repository_chunks(self, repository_id, chunks):
        self.replacement_calls.append(
            (repository_id, list(chunks))
        )

        self.chunks = [
            chunk
            for chunk in self.chunks
            if chunk.repository_id != repository_id
        ]
        self.chunks.extend(chunks)


class FakeSymbolRetrievalService:
    def __init__(self):
        self.symbols = []
        self.replacement_calls = []

    async def replace_repository_symbols(self, repository_id, symbols):
        self.replacement_calls.append(
            (repository_id, list(symbols))
        )

        self.symbols = [
            symbol
            for symbol in self.symbols
            if symbol.repository_id != repository_id
        ]
        self.symbols.extend(symbols)


class FakeRepositoryAnalyzer:
    def analyze(self, **kwargs):
        pass


def make_chunk(repository_id, chunk_id, content):
    return CodeChunk(
        chunk_id=chunk_id,
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path="src/model.py",
        source="repository",
        language="python",
        content=content,
        start_line=1,
        end_line=2,
    )


def make_symbol(repository_id, symbol_name):
    return CodeSymbol(
        symbol_id=f"{repository_id}-{symbol_name}",
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path="src/model.py",
        symbol_name=symbol_name,
        symbol_type="class",
        code=f"class {symbol_name}: pass",
        start_line=1,
        end_line=2,
    )


def test_reingestion_replaces_repository_state_and_preserves_others(
    tmp_path,
    monkeypatch,
):
    repository_root = tmp_path / "repo-a"
    repository_root.mkdir()

    repository = RepositoryInfo(
        repository_id=REPOSITORY_ID,
        repository_name="repo-a",
        repository_root=repository_root,
        branch="main",
        source="local",
        original_location=str(repository_root),
    )

    source = FakeSource(repository)

    monkeypatch.setattr(
        "app.code_ingestion.ingestion_service.RepositorySourceFactory.create",
        lambda location: source,
    )

    scanner = FakeScanner()
    chunker = FakeChunker()
    symbol_extractor = FakeSymbolExtractor()

    retrieval_service = FakeRetrievalService()
    symbol_retrieval_service = FakeSymbolRetrievalService()

    concept_index = ConceptIndex()
    concept_service = ConceptService(
        extractor=None,
        matcher=None,
    )

    repository_registry = RepositoryRegistry()

    service = CodeIngestionService(
        scanner=scanner,
        chunker=chunker,
        retrieval_service=retrieval_service,
        symbol_extractor=symbol_extractor,
        symbol_retrieval_service=symbol_retrieval_service,
        concept_service=concept_service,
        concept_index=concept_index,
        repository_analyzer=FakeRepositoryAnalyzer(),
        repository_registry=repository_registry,
    )

    retrieval_service.chunks.append(
        make_chunk(OTHER_REPOSITORY_ID, "other-chunk", "other content")
    )
    symbol_retrieval_service.symbols.append(
        make_symbol(OTHER_REPOSITORY_ID, "OtherModel")
    )
    concept_index.add(
        Concept(
            name="other",
            source="repository",
            repository_id=OTHER_REPOSITORY_ID,
        )
    )

    scanner.files = [repository_root / "src" / "model.py"]

    old_chunk = make_chunk(REPOSITORY_ID, "old-chunk", "old content")
    old_symbol = make_symbol(REPOSITORY_ID, "OldAttention")

    chunker.chunks = [old_chunk]
    symbol_extractor.symbols = [old_symbol]

    asyncio.run(service.ingest_repository(str(repository_root)))

    assert any(
        chunk.chunk_id == "old-chunk"
        for chunk in retrieval_service.chunks
    )
    assert concept_index.get("attention")[0].repository_id == REPOSITORY_ID

    new_chunk = make_chunk(REPOSITORY_ID, "new-chunk", "new content")
    new_symbol = make_symbol(REPOSITORY_ID, "NewEmbedding")

    chunker.chunks = [new_chunk]
    symbol_extractor.symbols = [new_symbol]

    asyncio.run(service.ingest_repository(str(repository_root)))

    repository_chunks = [
        chunk
        for chunk in retrieval_service.chunks
        if chunk.repository_id == REPOSITORY_ID
    ]
    assert [chunk.chunk_id for chunk in repository_chunks] == ["new-chunk"]

    repository_symbols = [
        symbol
        for symbol in symbol_retrieval_service.symbols
        if symbol.repository_id == REPOSITORY_ID
    ]
    assert [symbol.symbol_name for symbol in repository_symbols] == [
        "NewEmbedding"
    ]

    assert concept_index.get("attention") == []
    assert len(concept_index.get("embedding")) == 1
    assert concept_index.get("embedding")[0].repository_id == REPOSITORY_ID

    assert any(
        chunk.chunk_id == "other-chunk"
        for chunk in retrieval_service.chunks
    )
    assert any(
        symbol.symbol_name == "OtherModel"
        for symbol in symbol_retrieval_service.symbols
    )
    assert concept_index.get("other")[0].repository_id == OTHER_REPOSITORY_ID

    scanner.files = []
    chunker.chunks = []
    symbol_extractor.symbols = []

    asyncio.run(service.ingest_repository(str(repository_root)))

    assert not any(
        chunk.repository_id == REPOSITORY_ID
        for chunk in retrieval_service.chunks
    )
    assert not any(
        symbol.repository_id == REPOSITORY_ID
        for symbol in symbol_retrieval_service.symbols
    )
    assert concept_index.get("embedding") == []

    assert any(
        chunk.chunk_id == "other-chunk"
        for chunk in retrieval_service.chunks
    )
    assert concept_index.get("other")[0].repository_id == OTHER_REPOSITORY_ID

    assert len(retrieval_service.replacement_calls) == 3
    assert len(symbol_retrieval_service.replacement_calls) == 3
    registered = repository_registry.get(REPOSITORY_ID)

    assert registered is not None
    assert registered.repository_id == repository.repository_id
    assert registered.repository_name == repository.repository_name
    assert registered.repository_root == repository.repository_root.resolve()
