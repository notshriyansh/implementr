from typing import Literal

from pydantic import BaseModel


class RepositorySource(
    BaseModel,
):
    type: str


class LocalRepositoryModel(
    RepositorySource,
):
    type: Literal["local"] = "local"

    path: str


class GithubRepositoryModel(
    RepositorySource,
):
    type: Literal["github"] = "github"

    repository_url: str

    branch: str = "main"