from typing import Any

import numpy as np
from sentence_transformers import (
    SentenceTransformer,
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

    def embed_chunks(
        self,
        chunks: list[Any],
    ) -> np.ndarray:
        texts = [
            chunk.content
            if hasattr(
                chunk,
                "content",
            )
            else chunk.code
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