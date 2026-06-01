import numpy as np
from sentence_transformers import (
    SentenceTransformer,
)

from app.embeddings.base import (
    BaseEmbeddingModel,
)


class SentenceTransformerEmbeddingModel(
    BaseEmbeddingModel,
):
    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    async def embed_text(
        self,
        text: str,
    ) -> np.ndarray:
        embedding = self.model.encode(text)

        return np.array(embedding)

    async def embed_texts(
        self,
        texts: list[str],
    ) -> np.ndarray:
        embeddings = self.model.encode(texts)

        return np.array(embeddings)