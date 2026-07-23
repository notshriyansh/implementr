from __future__ import annotations

import logging
from typing import Generic, TypeVar
from uuid import uuid4

import numpy as np
from pydantic import BaseModel
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import FieldCondition
from qdrant_client.http.models import MatchValue

from app.vectorstores.base import BaseVectorStore

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class QdrantVectorStore(
    BaseVectorStore[T],
    Generic[T],
):
    def __init__(
        self,
        *,
        client: AsyncQdrantClient,
        collection_name: str,
        model: type[T],
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.model = model

    async def add(
        self,
        items: list[T],
        embeddings: np.ndarray,
    ) -> None:
        if not items:
            logger.info(
                "No items to upsert into '%s'.",
                self.collection_name,
            )
            return

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        if len(items) != len(embeddings):
            raise ValueError(
                "Number of items does not match number of embeddings."
            )

        points: list[PointStruct] = []

        for item, vector in zip(
            items,
            embeddings,
            strict=True,
        ):
            payload = item.model_dump()

            point_id = (
                payload.get("chunk_id")
                or payload.get("symbol_id")
                or payload.get("id")
                or str(uuid4())
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector.tolist(),
                    payload=payload,
                )
            )

        logger.info(
            "Upserting %d vectors into '%s'.",
            len(points),
            self.collection_name,
        )

        await self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

        logger.info(
            "Finished upserting into '%s'.",
            self.collection_name,
        )

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[T]:
        query_embedding = (
            np.asarray(
                query_embedding,
                dtype=np.float32,
            )
            .reshape(-1)
        )

        results = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=k,
        )

        return [
            self.model.model_validate(point.payload)
            for point in results.points
        ]

    async def delete_by_field(
        self,
        field: str,
        value: str,
    ) -> None:
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key=field,
                        match=MatchValue(
                            value=value,
                        ),
                    )
                ]
            ),
            wait=True,
        )

    async def count(self) -> int:
        result = await self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        return result.count

    async def clear(self) -> None:
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(),
            wait=True,
        )