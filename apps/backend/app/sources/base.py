from abc import ABC
from abc import abstractmethod

from pathlib import Path

from app.sources.models import (
    RepositorySource,
)


class BaseRepositorySource(
    ABC,
):
    def __init__(
        self,
        source: RepositorySource,
    ):
        self.source = source

    @abstractmethod
    async def prepare(self) -> Path:
        """
        Return a local directory ready for ingestion.
        """

    async def cleanup(
        self,
    ) -> None:
        """
        Cleanup any temporary resources.

        Local repositories do nothing.
        """
        return