from pathlib import Path

from app.sources.base import (
    BaseRepositorySource,
)

from app.sources.models import (
    GithubRepositoryModel,
)


class GithubRepositorySource(
    BaseRepositorySource,
):
    source: GithubRepositoryModel

    def __init__(
        self,
        source: GithubRepositoryModel,
    ):
        self.source = source

    async def prepare(
        self,
    ) -> Path:
        raise NotImplementedError(
            "GithubRepositorySource not implemented yet."
        )