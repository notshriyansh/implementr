import asyncio
import numpy as np

from app.schemas.code_symbol import CodeSymbol
from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)


class FakeEmbeddingModel:
    def __init__(self):
        self.calls = []

    async def embed_query(self, query):
        self.calls.append(query)
        return [[0.5, 0.5]]

    async def embed_chunks(self, items):
        return [[1.0, 0.0] for _ in items]


class FakeVectorStore:
    def __init__(self):
        self.calls = []

    async def similarity_search(
        self,
        embedding,
        k=5,
        repository_id=None,
    ):
        self.calls.append(
            {
                "embedding": embedding,
                "k": k,
                "repository_id": repository_id,
            }
        )
        return []

    async def replace_repository(self, repository_id, embeddings, symbols):
        self.replacement_kwargs = {
            "repository_id": repository_id,
            "embeddings": embeddings,
            "symbols": symbols,
        }


def test_retrieve_forwards_repository_scope():
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore()
    service = SymbolRetrievalService(
        embedding_model,
        vector_store,
    )

    results = asyncio.run(
        service.retrieve(
            query="implement attention",
            k=10,
            repository_id="repo-a",
        )
    )

    assert results == []
    assert embedding_model.calls == ["implement attention"]
    assert vector_store.calls == [
        {
            "embedding": [[0.5, 0.5]],
            "k": 10,
            "repository_id": "repo-a",
        }
    ]


def test_retrieve_without_repository_scope_remains_compatible():
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore()
    service = SymbolRetrievalService(
        embedding_model,
        vector_store,
    )

    asyncio.run(
        service.retrieve("find entry point")
    )

    assert vector_store.calls[0]["k"] == 5
    assert vector_store.calls[0]["repository_id"] is None


def test_non_positive_k_skips_embedding_and_search():
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore()
    service = SymbolRetrievalService(
        embedding_model,
        vector_store,
    )

    results = asyncio.run(
        service.retrieve(
            query="find entry point",
            k=0,
            repository_id="repo-a",
        )
    )

    assert results == []
    assert embedding_model.calls == []
    assert vector_store.calls == []


def test_replace_repository_symbols_forwards_repository_and_embeddings():
    symbol = CodeSymbol(
        symbol_id="new-a1",
        repository_id="repo-a",
        repository_name="repo-a",
        relative_path="src/main.py",
        symbol_name="new_a1",
        symbol_type="function",
        code="def new_a1(): pass",
        start_line=1,
        end_line=1,
    )

    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore()
    service = SymbolRetrievalService(embedding_model, vector_store)

    asyncio.run(
        service.replace_repository_symbols("repo-a", [symbol])
    )

    assert vector_store.replacement_kwargs["repository_id"] == "repo-a"
    assert vector_store.replacement_kwargs["symbols"] == [symbol]
    assert vector_store.replacement_kwargs["embeddings"] == [
        [1.0, 0.0]
    ]