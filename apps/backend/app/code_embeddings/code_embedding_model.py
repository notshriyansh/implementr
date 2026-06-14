import numpy as np
from sentence_transformers import (
    SentenceTransformer,
)

from app.schemas.code_chunk import (
    CodeChunk,
)


class CodeEmbeddingModel:
    def __init__(
        self,
        model_name: str = (
            "all-MiniLM-L6-v2"
        ),
    ) -> None:
        self.model = SentenceTransformer(
            model_name
        )

    async def embed_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> np.ndarray:
        texts = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts
        )

        return np.array(
            embeddings,
            dtype="float32",
        )

    async def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        embedding = self.model.encode(
            [query]
        )

        return np.array(
            embedding,
            dtype="float32",
        )