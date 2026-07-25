from pathlib import Path
from uuid import uuid4

from app.core.config import get_settings
from app.sources.base import BaseRepositorySource
from app.sources.models import GithubRepositoryModel
from app.utils.git import clone_repository


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
        settings = get_settings()

        workspace = (
            Path(settings.repository_workspace)
            / "github"
        )

        workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        repository_directory = (
            workspace / uuid4().hex
        )

        clone_repository(
            repository_url=self.source.repository_url,
            destination=repository_directory,
            branch=self.source.branch,
        )

        return repository_directory