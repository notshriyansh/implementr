import asyncio

import httpx
import numpy as np

from app.core.config import get_settings
from app.embeddings.base import BaseEmbeddingModel


class JinaEmbeddingModel(BaseEmbeddingModel):
    def __init__(self) -> None:
        self.settings = get_settings()

        if not self.settings.jina_api_key:
            raise RuntimeError(
                "JINA_API_KEY is not configured."
            )

        self.client = httpx.AsyncClient(
            base_url="https://api.jina.ai/v1",
            timeout=httpx.Timeout(60.0),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
            ),
            headers={
                "Authorization": (
                    f"Bearer {self.settings.jina_api_key}"
                ),
                "Content-Type": "application/json",
            },
        )

    @property
    def embedding_dimension(self) -> int:
        return self.settings.jina_embedding_dimension

    async def close(self) -> None:
        await self.client.aclose()

    async def embed_text(
        self,
        text: str,
    ) -> np.ndarray:
        embeddings = await self.embed_texts(
            [text]
        )

        return embeddings[0]

    async def embed_texts(
        self,
        texts: list[str],
    ) -> np.ndarray:

        if not texts:
            texts = [
                text
                for text in texts
                if text.strip()
            ]
            return np.empty(
                (
                    0,
                    self.embedding_dimension,
                ),
                dtype=np.float32,
            )

        batch_size = (
            self.settings.jina_batch_size
        )

        all_embeddings: list[list[float]] = []

        for start in range(
            0,
            len(texts),
            batch_size,
        ):

            batch = texts[
                start : start + batch_size
            ]

            embeddings = await (
                self._embed_batch(
                    batch
                )
            )

            all_embeddings.extend(
                embeddings
            )

        return np.asarray(
            all_embeddings,
            dtype=np.float32,
        )
    

    async def _embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        payload = {
            "model": (
                self.settings
                .jina_embedding_model
            ),
            "input": texts,
            "embedding_type": "float",
        }

        retries = self.settings.jina_retry_count

        backoff = 1

        for attempt in range(
            retries,
        ):

            try:

                response = (
                    await self.client.post(
                        "/embeddings",
                        json=payload,
                    )
                )

                if (
                    response.status_code
                    in {
                        429,
                        500,
                        502,
                        503,
                        504,
                    }
                    and attempt
                    < retries - 1
                ):

                    await asyncio.sleep(
                        backoff
                    )

                    backoff *= 2

                    continue

                if response.is_error:
                    raise RuntimeError(
                        f"Jina embedding request failed "
                        f"({response.status_code}): "
                        f"{response.text}"
                    )

                data = response.json()["data"]

                embeddings = [
                    item["embedding"]
                    for item in data
                ]

                if embeddings:
                    actual_dimension = len(
                        embeddings[0]
                    )

                    if (
                        actual_dimension
                        != self.embedding_dimension
                    ):
                        raise RuntimeError(
                            "Embedding dimension mismatch. "
                            f"Expected {self.embedding_dimension}, "
                            f"received {actual_dimension}."
                        )

                print(
                    "Returned embedding dimension:",
                    len(embeddings[0]),
                )

                return embeddings

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
            ):

                if (
                    attempt
                    == retries - 1
                ):
                    raise

                await asyncio.sleep(
                    backoff
                )

                await asyncio.sleep(
                    min(backoff, 8)
                )

                backoff *= 2

        raise RuntimeError(
            "Failed to generate embeddings from Jina."
        )