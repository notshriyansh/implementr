from typing import Any

import numpy as np
from app.embeddings.base import BaseEmbeddingModel


class CodeEmbeddingModel:

    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
    ) -> None:
        self.embedding_model = embedding_model

    def symbol_to_text(
        self,
        symbol: Any,
    ) -> str:
        return (
            f"""
        Repository:
        {symbol.repository_name}

        File:
        {symbol.relative_path}

        Symbol:
        {symbol.symbol_name}

        Type:
        {symbol.symbol_type}

        Code:

        {symbol.code}
        """
        )

    async def embed_chunks(
        self,
        chunks: list[Any],
    ) -> np.ndarray:

        texts: list[str] = []

        for chunk in chunks:
            if hasattr(chunk, "symbol_name"):
                texts.append(self.symbol_to_text(chunk))
            elif hasattr(chunk, "content"):
                texts.append(
                    f"""
                Repository:
                {chunk.repository_name}

                File:
                {chunk.relative_path}

                Language:
                {chunk.language}

                Code:

                {chunk.content}
                """
                )
            elif hasattr(chunk, "code"):
                texts.append(chunk.code)
            else:
                texts.append(str(chunk))

        return await self.embedding_model.embed_texts(
            texts
        )
    async def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        embedding = await self.embedding_model.embed_text(
            query
        )

        return embedding.reshape(1, -1)