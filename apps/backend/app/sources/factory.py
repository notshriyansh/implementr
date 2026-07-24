from app.sources.base import (
    BaseRepositorySource,
)

from app.sources.local import (
    LocalRepositorySource,
    LocalRepositoryModel,
)

from app.sources.github import (
    GithubRepositorySource,
)

from app.sources.models import (
    RepositorySource,
)

from app.sources.github import (
    GithubRepositoryModel,
)


class RepositorySourceFactory:

    @staticmethod
    def create(
        source: RepositorySource,
    ) -> BaseRepositorySource:

        if source.type == "local":
            return LocalRepositorySource(
                source
            )

        if source.type == "github":
            return GithubRepositorySource(
                source
            )

        raise ValueError(
            f"Unsupported repository source: {source.type}"
        )

    @staticmethod
    def create_from_dict(
        data: dict,
    ):
        type_ = data["type"]

        if type_ == "local":

            model = LocalRepositoryModel.model_validate(
                data
            )

            return RepositorySourceFactory.create(model)

        if type_ == "github":

            model = GithubRepositoryModel.model_validate(
                data
            )

            return RepositorySourceFactory.create(model)

        raise ValueError(
            f"Unsupported repository source type: {type_}"
        )