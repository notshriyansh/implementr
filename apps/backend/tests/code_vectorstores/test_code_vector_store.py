import asyncio

import faiss
import json
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


# ---------------------------------------------------------------------------
# Repository replacement regression tests
# ---------------------------------------------------------------------------


@pytest.fixture
def persistent_store(tmp_path, monkeypatch):
    monkeypatch.setattr(
        CodeVectorStore,
        "INDEX_PATH",
        tmp_path / "code.index",
    )
    monkeypatch.setattr(
        CodeVectorStore,
        "METADATA_PATH",
        tmp_path / "chunks.json",
    )

    return CodeVectorStore(embedding_dimension=2)


def make_embeddings(vectors: list[list[float]]) -> np.ndarray:
    return np.asarray(vectors, dtype=np.float32).reshape(-1, 2)


def test_replace_repository_removes_old_chunks_and_indexes_new_chunks(
    persistent_store,
):
    store = persistent_store

    asyncio.run(
        store.add_embeddings(
            make_embeddings([
                [1.0, 0.0],
                [0.0, 1.0],
            ]),
            [
                make_chunk("old-a1", "repo-a"),
                make_chunk("keep-b1", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            repository_id="repo-a",
            embeddings=make_embeddings([
                [0.0, 1.0],
            ]),
            chunks=[
                make_chunk("new-a1", "repo-a"),
            ],
        )
    )

    assert [chunk.chunk_id for chunk in store.chunks] == [
        "keep-b1",
        "new-a1",
    ]
    assert store.index.ntotal == 2

    results = asyncio.run(
        store.similarity_search(
            query_embedding=make_embeddings([[0.0, 1.0]]),
            k=5,
            repository_id="repo-a",
        )
    )

    assert [chunk.chunk_id for chunk in results] == ["new-a1"]


def test_replace_repository_preserves_other_repository_search_results(
    persistent_store,
):
    store = persistent_store

    asyncio.run(
        store.add_embeddings(
            make_embeddings([
                [1.0, 0.0],
                [0.0, 1.0],
            ]),
            [
                make_chunk("old-a1", "repo-a"),
                make_chunk("keep-b1", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            repository_id="repo-a",
            embeddings=make_embeddings([
                [0.0, 1.0],
            ]),
            chunks=[
                make_chunk("new-a1", "repo-a"),
            ],
        )
    )

    results = asyncio.run(
        store.similarity_search(
            query_embedding=make_embeddings([[0.0, 1.0]]),
            k=5,
            repository_id="repo-b",
        )
    )

    assert [chunk.chunk_id for chunk in results] == ["keep-b1"]


def test_replace_repository_with_empty_chunks_removes_repository_data(
    persistent_store,
):
    store = persistent_store

    asyncio.run(
        store.add_embeddings(
            make_embeddings([
                [1.0, 0.0],
                [0.0, 1.0],
            ]),
            [
                make_chunk("old-a1", "repo-a"),
                make_chunk("keep-b1", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            repository_id="repo-a",
            embeddings=make_embeddings([]),
            chunks=[],
        )
    )

    assert [chunk.chunk_id for chunk in store.chunks] == ["keep-b1"]
    assert store.index.ntotal == 1

    results = asyncio.run(
        store.similarity_search(
            query_embedding=make_embeddings([[1.0, 0.0]]),
            k=5,
            repository_id="repo-a",
        )
    )

    assert results == []


def test_replace_repository_persists_consistent_index_and_metadata(
    persistent_store,
):
    store = persistent_store

    asyncio.run(
        store.add_embeddings(
            make_embeddings([
                [1.0, 0.0],
                [0.0, 1.0],
            ]),
            [
                make_chunk("old-a1", "repo-a"),
                make_chunk("keep-b1", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            repository_id="repo-a",
            embeddings=make_embeddings([
                [0.6, 0.8],
                [0.8, 0.6],
            ]),
            chunks=[
                make_chunk("new-a1", "repo-a"),
                make_chunk("new-a2", "repo-a"),
            ],
        )
    )

    persisted_index = faiss.read_index(str(store.INDEX_PATH))

    persisted_chunks = [
        CodeChunk(**item)
        for item in json.loads(store.METADATA_PATH.read_text())
    ]

    assert persisted_index.ntotal == 3
    assert len(persisted_chunks) == 3

    assert {
        chunk.chunk_id for chunk in persisted_chunks
    } == {
        "keep-b1",
        "new-a1",
        "new-a2",
    }


def test_reloaded_store_retains_replaced_repository_data(
    persistent_store,
):
    store = persistent_store

    asyncio.run(
        store.add_embeddings(
            make_embeddings([
                [1.0, 0.0],
                [0.0, 1.0],
            ]),
            [
                make_chunk("old-a1", "repo-a"),
                make_chunk("keep-b1", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            repository_id="repo-a",
            embeddings=make_embeddings([
                [0.6, 0.8],
            ]),
            chunks=[
                make_chunk("new-a1", "repo-a"),
            ],
        )
    )

    reloaded_store = CodeVectorStore(embedding_dimension=2)

    assert reloaded_store.index.ntotal == 2
    assert {
        chunk.chunk_id for chunk in reloaded_store.chunks
    } == {
        "keep-b1",
        "new-a1",
    }

    results = asyncio.run(
        reloaded_store.similarity_search(
            query_embedding=make_embeddings([[0.6, 0.8]]),
            k=5,
            repository_id="repo-a",
        )
    )

    assert [chunk.chunk_id for chunk in results] == ["new-a1"]


def test_replace_repository_rejects_inconsistent_index_and_metadata(
    persistent_store,
):
    store = persistent_store

    asyncio.run(
        store.add_embeddings(
            make_embeddings([[1.0, 0.0]]),
            [make_chunk("old-a1", "repo-a")],
        )
    )

    store.index.add(make_embeddings([[0.0, 1.0]]))

    original_index = store.index
    original_chunks = list(store.chunks)

    with pytest.raises(ValueError, match="index and metadata are inconsistent"):
        asyncio.run(
            store.replace_repository(
                repository_id="repo-a",
                embeddings=make_embeddings([[0.0, 1.0]]),
                chunks=[make_chunk("new-a1", "repo-a")],
            )
        )

    assert store.index is original_index
    assert store.chunks == original_chunks
