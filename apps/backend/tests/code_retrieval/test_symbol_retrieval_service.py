import asyncio

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)


class FakeEmbeddingModel:
    def __init__(self):
        self.calls = []

    async def embed_query(self, query):
        self.calls.append(query)
        return [[0.5, 0.5]]


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