import asyncio

import numpy as np
import pytest

from app.code_vectorstores.code_vector_store import CodeVectorStore
from app.schemas.code_chunk import CodeChunk


def make_chunk(chunk_id: str, repository_id: str) -> CodeChunk:
    return CodeChunk(
        chunk_id=chunk_id,
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path=f"src/{chunk_id}.py",
        source="repository",
        branch="main",
        language="python",
        content=f"# {chunk_id}",
        start_line=1,
        end_line=1,
    )


class FakeIndex:
    ntotal = 4

    def search(self, query_embedding, k):
        ranked_indices = [0, 1, 2, 3][:k]
        scores = np.array(
            [[0.9, 0.8, 0.7, 0.6][:k]],
            dtype=np.float32,
        )
        indices = np.array([ranked_indices], dtype=np.int64)
        return scores, indices


@pytest.fixture
def store():
    instance = CodeVectorStore.__new__(CodeVectorStore)
    instance.index = FakeIndex()
    instance.chunks = [
        make_chunk("a", "repo-a"),
        make_chunk("b", "repo-b"),
        make_chunk("c", "repo-a"),
        make_chunk("d", "repo-b"),
    ]
    return instance


def test_scoped_search_returns_only_requested_repository(store):
    results = asyncio.run(
        store.similarity_search(
            query_embedding=np.array([[1.0, 0.0]], dtype=np.float32),
            k=2,
            repository_id="repo-a",
        )
    )

    assert [chunk.chunk_id for chunk in results] == ["a", "c"]
    assert all(chunk.repository_id == "repo-a" for chunk in results)


def test_global_search_preserves_top_k_behavior(store):
    results = asyncio.run(
        store.similarity_search(
            query_embedding=np.array([[1.0, 0.0]], dtype=np.float32),
            k=2,
        )
    )

    assert [chunk.chunk_id for chunk in results] == ["a", "b"]


def test_scoped_search_returns_empty_when_repository_has_no_matches(store):
    results = asyncio.run(
        store.similarity_search(
            query_embedding=np.array([[1.0, 0.0]], dtype=np.float32),
            k=2,
            repository_id="repo-missing",
        )
    )

    assert results == []


def test_search_returns_empty_for_nonpositive_k(store):
    results = asyncio.run(
        store.similarity_search(
            query_embedding=np.array([[1.0, 0.0]], dtype=np.float32),
            k=0,
            repository_id="repo-a",
        )
    )

    assert results == []


def test_scoped_search_returns_all_repository_candidates_for_deduplication(store):
    store.chunks = [
        make_chunk("a1", "repo-a"),
        make_chunk("a2", "repo-a"),
        make_chunk("a3", "repo-a"),
        make_chunk("b1", "repo-b"),
    ]
    store.index.ntotal = 4

    results = asyncio.run(
        store.similarity_search(
            query_embedding=np.array([[1.0, 0.0]], dtype=np.float32),
            k=2,
            repository_id="repo-a",
        )
    )

    assert [chunk.chunk_id for chunk in results] == ["a1", "a2", "a3"]
    assert all(chunk.repository_id == "repo-a" for chunk in results)

