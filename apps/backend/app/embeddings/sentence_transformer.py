
import numpy as np
from sentence_transformers import SentenceTransformer

from app.embeddings.base import BaseEmbeddingModel


class SentenceTransformerEmbeddingModel(
    BaseEmbeddingModel
):
    EMBED_BATCH_SIZE = 256
    MODEL_BATCH_SIZE = 128

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(
            model_name
        )

    async def embed_text(
        self,
        text: str,
    ) -> np.ndarray:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return np.asarray(
            embedding,
            dtype=np.float32,
        )

    async def embed_texts(
        self,
        texts: list[str],
    ) -> np.ndarray:

        if not texts:
            return np.empty(
                (
                    0,
                    self.model.get_sentence_embedding_dimension(),
                ),
                dtype=np.float32,
            )

        embeddings: list[np.ndarray] = []

        for i in range(
            0,
            len(texts),
            self.EMBED_BATCH_SIZE,
        ):

            batch = texts[
                i : i + self.EMBED_BATCH_SIZE
            ]

            batch_embeddings = self.model.encode(
                batch,
                batch_size=self.MODEL_BATCH_SIZE,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            embeddings.append(batch_embeddings)

        return np.asarray(
            np.vstack(embeddings),
            dtype=np.float32,
        )