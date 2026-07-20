import numpy as np

from app.embeddings.base import BaseEmbeddingModel


class SentenceTransformerEmbeddingModel(BaseEmbeddingModel):
    DIMENSION = 384

    async def embed_text(
        self,
        text: str,
    ) -> np.ndarray:
        return np.random.rand(self.DIMENSION).astype(np.float32)

    async def embed_texts(
        self,
        texts: list[str],
    ) -> np.ndarray:
        return np.random.rand(
            len(texts),
            self.DIMENSION,
        ).astype(np.float32)