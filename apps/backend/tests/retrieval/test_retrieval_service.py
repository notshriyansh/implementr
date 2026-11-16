
import asyncio

import numpy as np

from app.retrieval.retrieval_service import RetrievalService
from app.schemas.chunk import DocumentChunk


def make_chunk(
    chunk_id: str,
    paper_id: str,
    text: str,
    chunk_index: int = 0,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        text=text,
        page_number=1,
        chunk_index=chunk_index,
        paper_id=paper_id,
        user_id="test_user",
    )


class FakeEmbeddingModel:
    async def embed_text(self, text: str):
        return np.asarray([0.1, 0.2, 0.3], dtype="float32")


class FakeVectorStore:
    def __init__(self, results=None):
        self.results = results or []
        self.calls = []

    async def similarity_search(
        self,
        query_embedding,
        k=5,
        paper_id=None,
    ):
        self.calls.append(
            {
                "query_embedding": query_embedding,
                "k": k,
                "paper_id": paper_id,
            }
        )
        return self.results


def test_retrieve_forwards_paper_id_to_vector_store():
    chunks = [
        make_chunk(
            "chunk-1",
            "paper-A",
            "First relevant chunk",
            chunk_index=0,
        ),
        make_chunk(
            "chunk-2",
            "paper-A",
            "Second relevant chunk",
            chunk_index=1,
        ),
    ]

    vector_store = FakeVectorStore(results=chunks)

    service = RetrievalService(
        embedding_model=FakeEmbeddingModel(),
        vector_store=vector_store,
    )

    results = asyncio.run(
        service.retrieve(
            query="Explain the paper's approach",
            k=2,
            paper_id="paper-A",
        )
    )

    assert len(results) == 2
    assert vector_store.calls[0]["paper_id"] == "paper-A"
    assert vector_store.calls[0]["k"] == 2
    assert vector_store.calls[0]["query_embedding"].shape == (1, 3)


def test_retrieve_without_paper_id_preserves_global_behavior():
    chunks = [
        make_chunk("chunk-1", "paper-A", "Paper A content"),
        make_chunk("chunk-2", "paper-B", "Paper B content"),
    ]

    vector_store = FakeVectorStore(results=chunks)

    service = RetrievalService(
        embedding_model=FakeEmbeddingModel(),
        vector_store=vector_store,
    )

    results = asyncio.run(
        service.retrieve(
            query="Explain the retrieval approach",
            k=5,
        )
    )

    assert len(results) == 2
    assert vector_store.calls[0]["paper_id"] is None
    assert vector_store.calls[0]["k"] == 5


def test_retrieve_returns_empty_when_vector_store_has_no_results():
    vector_store = FakeVectorStore(results=[])

    service = RetrievalService(
        embedding_model=FakeEmbeddingModel(),
        vector_store=vector_store,
    )

    results = asyncio.run(
        service.retrieve(
            query="A query with no matching chunks",
            paper_id="paper-A",
        )
    )

    assert results == []
