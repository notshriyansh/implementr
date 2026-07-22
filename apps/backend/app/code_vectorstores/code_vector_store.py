import faiss
import numpy as np

from app.schemas.code_chunk import CodeChunk
from app.vectorstores.base import BaseVectorStore


class CodeVectorStore(
    BaseVectorStore[CodeChunk],
):
    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:
        self.index = faiss.IndexFlatIP(
            embedding_dimension,
        )

        self.chunks: list[CodeChunk] = []

    async def add(
        self,
        items: list[CodeChunk],
        embeddings: np.ndarray,
    ) -> None:
        embeddings = embeddings.astype("float32")

        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        print(
            f"Indexed {self.index.ntotal} code vectors."
        )

        self.chunks.extend(items)

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[CodeChunk]:
        query_embedding = (
            np.asarray(
                query_embedding,
                dtype=np.float32,
            )
            .reshape(1, -1)
        )

        faiss.normalize_L2(
            query_embedding
        )

        _, indices = self.index.search(
            query_embedding,
            k,
        )

        results: list[CodeChunk] = []

        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])

        return results