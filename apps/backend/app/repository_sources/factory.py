from urllib.parse import urlsplit

from app.repository_sources.base import RepositorySource
from app.repository_sources.github import GitHubRepositorySource


class RepositorySourceFactory:
    @staticmethod
    def create(location: str) -> RepositorySource:
        location = location.strip()

        if not location:
            raise ValueError("Repository location cannot be empty")

        try:
            parsed = urlsplit(location)
            hostname = parsed.hostname
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Invalid GitHub repository URL") from exc

        if (
            parsed.scheme != "https"
            or hostname != "github.com"
            or port not in (None, 443)
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Only HTTPS GitHub repository URLs are supported")

        path_parts = parsed.path.strip("/").split("/")

        if len(path_parts) != 2:
            raise ValueError(
                "Expected a GitHub URL in the format https://github.com/owner/repository"
            )

        owner, repository = path_parts
        repository = repository.removesuffix(".git")

        if (
            not owner
            or not repository
            or owner in {".", ".."}
            or repository in {".", ".."}
            or not all(
                character.isascii()
                and (character.isalnum() or character in "-_.")
                for character in owner + repository
            )
        ):
            raise ValueError("Invalid GitHub owner or repository name")

        return GitHubRepositorySource()
