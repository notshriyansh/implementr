from app.repository_sources.github import (
    GitHubRepositorySource,
)

from app.repository_sources.local import (
    LocalRepositorySource,
)

from app.repository_sources.base import (
    RepositorySource,
)


class RepositorySourceFactory:

    @staticmethod
    def create(
        location: str,
    ) -> RepositorySource:

        location = location.strip()

        if (
            "github.com" in location.lower()
        ):
            return GitHubRepositorySource()

        return LocalRepositorySource()