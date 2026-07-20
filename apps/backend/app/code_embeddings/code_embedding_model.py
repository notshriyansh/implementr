import gc
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer


class CodeEmbeddingModel:
    EMBED_BATCH_SIZE = 8

    MODEL_BATCH_SIZE = 4

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def symbol_to_text(
        self,
        symbol: Any,
    ) -> str:
        return (
            f"Symbol Name: {symbol.symbol_name}\n"
            f"Symbol Type: {symbol.symbol_type}\n"
            f"File: {Path(symbol.file_path).stem}"
        )

    def embed_chunks(
        self,
        chunks: list[Any],
    ) -> np.ndarray:

        embeddings = []

        for i in range(
            0,
            len(chunks),
            self.EMBED_BATCH_SIZE,
        ):

            batch_chunks = chunks[
                i : i + self.EMBED_BATCH_SIZE
            ]

            batch_texts = []

            for chunk in batch_chunks:

                if hasattr(chunk, "symbol_name"):
                    batch_texts.append(
                        self.symbol_to_text(chunk)
                    )

                elif hasattr(chunk, "content"):
                    batch_texts.append(
                        chunk.content
                    )

                elif hasattr(chunk, "code"):
                    batch_texts.append(
                        chunk.code
                    )

                else:
                    batch_texts.append(
                        str(chunk)
                    )

            batch_embeddings = self.model.encode(
                batch_texts,
                batch_size=self.MODEL_BATCH_SIZE,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            embeddings.append(batch_embeddings)

            del batch_chunks
            del batch_texts
            del batch_embeddings

            gc.collect()

        return np.asarray(
            np.vstack(embeddings),
            dtype=np.float32,
        )