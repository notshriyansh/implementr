from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import numpy as np

T = TypeVar("T")


class BaseVectorStore(
    Generic[T],
    ABC,
):
    @abstractmethod
    async def add(
        self,
        items: list[T],
        embeddings: np.ndarray,
    ) -> None:
        ...

    @abstractmethod
    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[T]:
        ...

    @abstractmethod
    async def delete_by_field(
        self,
        field: str,
        value: str,
    ) -> None:
        ...

    @abstractmethod
    async def count(self) -> int:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...