import asyncio

import faiss
import numpy as np

from app.schemas.chunk import DocumentChunk
from app.vectorstores.faiss_store import FAISSVectorStore


def make_chunk(
    chunk_id: str,
    paper_id: str,
    text: str,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        text=text,
        page_number=1,
        chunk_index=0,
        paper_id=paper_id,
        user_id="test_user",
    )


def make_store(vectors: list[list[float]], chunks: list[DocumentChunk]):
    """
    Build a FAISSVectorStore without invoking its persistence-related
    constructor logic. The test uses a real IndexFlatL2 index.
    """
    store = FAISSVectorStore.__new__(FAISSVectorStore)

    store.index = faiss.IndexFlatL2(len(vectors[0]))
    store.index.add(np.asarray(vectors, dtype="float32"))
    store.chunks = chunks

    return store


def test_similarity_search_returns_only_selected_paper_chunks():
    chunks = [
        make_chunk("chunk-1", "paper-A", "Paper A content"),
        make_chunk("chunk-2", "paper-B", "Paper B content"),
        make_chunk("chunk-3", "paper-A", "More Paper A content"),
    ]

    store = make_store(
        vectors=[
            [0.1, 0.0],   # Paper A
            [0.0, 0.0],   # Paper B
            [0.2, 0.0],   # Paper A
        ],
        chunks=chunks,
    )

    query_embedding = np.asarray([[0.0, 0.0]], dtype="float32")

    results = asyncio.run(
        store.similarity_search(
            query_embedding=query_embedding,
            k=1,
            paper_id="paper-A",
        )
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].paper_id == "paper-A"


def test_similarity_search_returns_k_nearest_chunks_from_selected_paper():
    chunks = [
        make_chunk("chunk-1", "paper-A", "A1"),
        make_chunk("chunk-2", "paper-B", "B1"),
        make_chunk("chunk-3", "paper-A", "A2"),
        make_chunk("chunk-4", "paper-A", "A3"),
    ]

    store = make_store(
        vectors=[
            [0.1, 0.0],   # A1
            [0.0, 0.0],   # B1
            [0.3, 0.0],   # A2
            [0.5, 0.0],   # A3
        ],
        chunks=chunks,
    )

    query_embedding = np.asarray([[0.0, 0.0]], dtype="float32")

    results = asyncio.run(
        store.similarity_search(
            query_embedding=query_embedding,
            k=2,
            paper_id="paper-A",
        )
    )

    assert len(results) == 2
    assert [chunk.chunk_id for chunk in results] == [
        "chunk-1",
        "chunk-3",
    ]
    assert all(chunk.paper_id == "paper-A" for chunk in results)


def test_similarity_search_without_paper_id_preserves_global_behavior():
    chunks = [
        make_chunk("chunk-1", "paper-A", "A1"),
        make_chunk("chunk-2", "paper-B", "B1"),
        make_chunk("chunk-3", "paper-A", "A2"),
    ]

    store = make_store(
        vectors=[
            [0.1, 0.0],
            [0.0, 0.0],
            [0.2, 0.0],
        ],
        chunks=chunks,
    )

    query_embedding = np.asarray([[0.0, 0.0]], dtype="float32")

    results = asyncio.run(
        store.similarity_search(
            query_embedding=query_embedding,
            k=2,
        )
    )

    assert len(results) == 2
    assert [chunk.chunk_id for chunk in results] == [
        "chunk-2",
        "chunk-1",
    ]


def test_similarity_search_returns_empty_for_unknown_paper():
    chunks = [
        make_chunk("chunk-1", "paper-A", "A1"),
        make_chunk("chunk-2", "paper-B", "B1"),
    ]

    store = make_store(
        vectors=[
            [0.1, 0.0],
            [0.2, 0.0],
        ],
        chunks=chunks,
    )

    query_embedding = np.asarray([[0.0, 0.0]], dtype="float32")

    results = asyncio.run(
        store.similarity_search(
            query_embedding=query_embedding,
            k=5,
            paper_id="paper-does-not-exist",
        )
    )

    assert results == []


def test_similarity_search_returns_empty_when_k_is_zero():
    chunks = [
        make_chunk("chunk-1", "paper-A", "A1"),
    ]

    store = make_store(
        vectors=[[0.1, 0.0]],
        chunks=chunks,
    )

    query_embedding = np.asarray([[0.0, 0.0]], dtype="float32")

    results = asyncio.run(
        store.similarity_search(
            query_embedding=query_embedding,
            k=0,
            paper_id="paper-A",
        )
    )

    assert results == []
