from abc import ABC
from abc import abstractmethod

from app.repository_sources.repository_info import (
    RepositoryInfo,
)


class RepositorySource(ABC):

    @abstractmethod
    async def prepare(
        self,
        location: str,
    ) -> RepositoryInfo:
        pass

    async def cleanup(
        self,
    ) -> None:
        return