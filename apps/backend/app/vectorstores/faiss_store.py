import faiss
import numpy as np

from app.schemas.chunk import DocumentChunk
from app.vectorstores.base import (
    BaseVectorStore,
)


class FAISSVectorStore(
    BaseVectorStore,
):
    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:
        self.index = faiss.IndexFlatL2(
            embedding_dimension
        )

        self.chunks: list[DocumentChunk] = []

    async def add_embeddings(
        self,
        embeddings: np.ndarray,
        chunks: list[DocumentChunk],
    ) -> None:
        self.index.add(
            embeddings.astype("float32")
        )

        self.chunks.extend(chunks)

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[DocumentChunk]:
        distances, indices = self.index.search(
            query_embedding.astype("float32"),
            k,
        )

        results: list[DocumentChunk] = []

        for index in indices[0]:
            if index < len(self.chunks):
                results.append(
                    self.chunks[index]
                )

        return results