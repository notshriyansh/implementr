from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer


class CodeEmbeddingModel:
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
        texts: list[str] = []

        for chunk in chunks:
            if hasattr(chunk, "symbol_name"):
                texts.append(self.symbol_to_text(chunk))
            elif hasattr(chunk, "content"):
                texts.append(chunk.content)
            elif hasattr(chunk, "code"):
                texts.append(chunk.code)
            else:
                texts.append(str(chunk))

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return np.asarray(
            embeddings,
            dtype=np.float32,
        )

    async def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )

        return np.asarray(
            embedding,
            dtype=np.float32,
        )