import asyncio

import math
import os
import time
from collections import deque
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

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

        self.max_tokens_per_minute = int(
            os.getenv("JINA_MAX_TOKENS_PER_MINUTE", "70000")
        )
        self.chars_per_estimated_token = float(
            os.getenv("JINA_CHARS_PER_ESTIMATED_TOKEN", "3.0")
        )

        if self.max_tokens_per_minute < 1:
            raise ValueError("JINA_MAX_TOKENS_PER_MINUTE must be positive")
        if self.chars_per_estimated_token <= 0:
            raise ValueError("JINA_CHARS_PER_ESTIMATED_TOKEN must be positive")

        self._token_usage: deque[tuple[float, int]] = deque()
        self._token_budget_lock = asyncio.Lock()

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

    
    def _estimate_tokens(self, text: str) -> int:
        return max(
            1,
            math.ceil(len(text) / self.chars_per_estimated_token),
        )

    async def _reserve_token_budget(self, estimated_tokens: int) -> None:
        if estimated_tokens > self.max_tokens_per_minute:
            raise ValueError(
                "A single embedding batch exceeds the configured token budget. "
                "Reduce the input size or increase the budget deliberately."
            )

        while True:
            async with self._token_budget_lock:
                now = time.monotonic()

                while (
                    self._token_usage
                    and now - self._token_usage[0][0] >= 60
                ):
                    self._token_usage.popleft()

                used = sum(tokens for _, tokens in self._token_usage)

                if used + estimated_tokens <= self.max_tokens_per_minute:
                    self._token_usage.append((now, estimated_tokens))
                    return

                wait_seconds = max(
                    0.1,
                    60 - (now - self._token_usage[0][0]) + 0.1,
                )

            print(
                f"Jina token budget reached; waiting "
                f"{wait_seconds:.1f}s before the next request."
            )
            await asyncio.sleep(wait_seconds)

    @staticmethod
    def _retry_after_seconds(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")
        if not value:
            return None

        try:
            return max(0.0, float(value))
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(value)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(
                    0.0,
                    (retry_at - datetime.now(timezone.utc)).total_seconds(),
                )
            except (TypeError, ValueError, OverflowError):
                return None

    async def embed_texts(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty(
                (0, self.embedding_dimension),
                dtype=np.float32,
            )

        max_items = max(1, self.settings.jina_batch_size)
        batches: list[list[str]] = []
        current_batch: list[str] = []
        current_tokens = 0

        for text in texts:
            estimated = self._estimate_tokens(text)

            if estimated > self.max_tokens_per_minute:
                raise ValueError(
                    "A single text exceeds the configured token budget. "
                    "Reduce or split the source text before embedding."
                )

            should_flush = current_batch and (
                len(current_batch) >= max_items
                or current_tokens + estimated > self.max_tokens_per_minute
            )

            if should_flush:
                batches.append(current_batch)
                current_batch = []
                current_tokens = 0

            current_batch.append(text)
            current_tokens += estimated

        if current_batch:
            batches.append(current_batch)

        all_embeddings: list[list[float]] = []

        for batch in batches:
            all_embeddings.extend(await self._embed_batch(batch))

        return np.asarray(all_embeddings, dtype=np.float32)

    async def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        payload = {
            "model": self.settings.jina_embedding_model,
            "input": texts,
            "embedding_type": "float",
        }

        estimated_tokens = sum(
            self._estimate_tokens(text) for text in texts
        )
        retries = max(1, self.settings.jina_retry_count)
        retryable_statuses = {429, 500, 502, 503, 504}

        for attempt in range(retries):
            await self._reserve_token_budget(estimated_tokens)

            try:
                response = await self.client.post(
                    "/embeddings",
                    json=payload,
                )
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(min(2 ** attempt, 8))
                continue

            if response.status_code in retryable_statuses:
                if attempt == retries - 1:
                    raise RuntimeError(
                        f"Jina embedding request failed "
                        f"({response.status_code}) after {retries} attempts: "
                        f"{response.text}"
                    )

                retry_after = self._retry_after_seconds(response)
                backoff = min(2 ** attempt, 8)
                delay = max(backoff, retry_after or 0.0)

                if response.status_code == 429:
                    delay = max(delay, 5.0)

                await asyncio.sleep(delay)
                continue

            if response.is_error:
                raise RuntimeError(
                    f"Jina embedding request failed "
                    f"({response.status_code}): {response.text}"
                )

            data = response.json().get("data", [])
            embeddings = [item["embedding"] for item in data]

            if len(embeddings) != len(texts):
                raise RuntimeError(
                    f"Jina returned {len(embeddings)} embeddings "
                    f"for {len(texts)} inputs."
                )

            if any(
                len(embedding) != self.embedding_dimension
                for embedding in embeddings
            ):
                raise RuntimeError(
                    f"Jina embedding dimension mismatch; expected "
                    f"{self.embedding_dimension}."
                )

            return embeddings

        raise RuntimeError("Jina embedding retries exhausted.")
