import asyncio

import numpy as np

from app.code_retrieval.code_retrieval_service import CodeRetrievalService
from app.schemas.code_chunk import CodeChunk


def make_chunk(
    chunk_id: str,
    repository_id: str,
    relative_path: str,
) -> CodeChunk:
    return CodeChunk(
        chunk_id=chunk_id,
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path=relative_path,
        source="repository",
        branch="main",
        language="python",
        content=f"# {chunk_id}",
        start_line=1,
        end_line=10,
    )


class FakeEmbeddingModel:
    def __init__(self):
        self.query_calls = 0

    async def embed_query(self, query: str) -> np.ndarray:
        self.query_calls += 1
        return np.array([[1.0, 0.0]], dtype=np.float32)

    async def embed_chunks(self, items):
        return np.ones((len(items), 2), dtype=np.float32)


class FakeVectorStore:
    def __init__(self, chunks: list[CodeChunk]):
        self.chunks = chunks
        self.search_kwargs = None

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        repository_id: str | None = None,
    ) -> list[CodeChunk]:
        self.search_kwargs = {
            "query_embedding": query_embedding,
            "k": k,
            "repository_id": repository_id,
        }

        return [
            chunk
            for chunk in self.chunks
            if repository_id is None
            or chunk.repository_id == repository_id
        ]

    async def replace_repository(self, repository_id, embeddings, chunks):
        self.replacement_kwargs = {
            "repository_id": repository_id,
            "embeddings": embeddings,
            "chunks": chunks,
        }


def test_retrieve_forwards_repository_filter_and_deduplicates_files():
    chunks = [
        make_chunk("a1", "repo-a", "src/main.py"),
        make_chunk("a2", "repo-a", "src/main.py"),
        make_chunk("b1", "repo-b", "src/main.py"),
        make_chunk("a3", "repo-a", "src/utils.py"),
    ]
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore(chunks)
    service = CodeRetrievalService(embedding_model, vector_store)

    results = asyncio.run(
        service.retrieve(
            query="find the main function",
            k=2,
            repository_id="repo-a",
        )
    )

    assert vector_store.search_kwargs["repository_id"] == "repo-a"
    assert vector_store.search_kwargs["k"] == 6
    assert embedding_model.query_calls == 1
    assert [chunk.chunk_id for chunk in results] == ["a1", "a3"]
    assert all(chunk.repository_id == "repo-a" for chunk in results)


def test_retrieve_without_repository_filter_preserves_global_search():
    chunks = [
        make_chunk("a1", "repo-a", "src/main.py"),
        make_chunk("b1", "repo-b", "src/main.py"),
    ]
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore(chunks)
    service = CodeRetrievalService(embedding_model, vector_store)

    results = asyncio.run(
        service.retrieve(query="find main", k=2)
    )

    assert vector_store.search_kwargs["repository_id"] is None
    assert [chunk.chunk_id for chunk in results] == ["a1", "b1"]


def test_retrieve_with_nonpositive_k_skips_embedding_and_search():
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore([])
    service = CodeRetrievalService(embedding_model, vector_store)

    results = asyncio.run(
        service.retrieve(query="find main", k=0, repository_id="repo-a")
    )

    assert results == []
    assert embedding_model.query_calls == 0
    assert vector_store.search_kwargs is None


def test_replace_repository_chunks_forwards_repository_and_embeddings():
    chunks = [
        make_chunk("new-a1", "repo-a", "src/main.py"),
        make_chunk("new-a2", "repo-a", "src/utils.py"),
    ]
    embedding_model = FakeEmbeddingModel()
    vector_store = FakeVectorStore([])
    service = CodeRetrievalService(embedding_model, vector_store)

    asyncio.run(
        service.replace_repository_chunks("repo-a", chunks)
    )

    assert vector_store.replacement_kwargs["repository_id"] == "repo-a"
    assert vector_store.replacement_kwargs["chunks"] == chunks
    assert vector_store.replacement_kwargs["embeddings"].shape == (2, 2)