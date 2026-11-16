import asyncio

import numpy as np

from app.code_embeddings.code_embedding_model import CodeEmbeddingModel


class FakeEmbeddingModel:
    embedding_dimension = 384

    async def embed_texts(self, texts):
        raise AssertionError(
            "Provider should not be called for empty input"
        )


def test_embed_chunks_returns_empty_array_for_empty_input():
    model = CodeEmbeddingModel(FakeEmbeddingModel())

    embeddings = asyncio.run(model.embed_chunks([]))

    assert embeddings.shape == (0, 384)
    assert embeddings.dtype == np.float32
