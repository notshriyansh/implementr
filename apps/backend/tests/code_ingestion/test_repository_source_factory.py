import pytest

from app.repository_sources.factory import RepositorySourceFactory
from app.repository_sources.github import GitHubRepositorySource


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/owner/repository",
        "https://github.com/owner/repository.git",
        "https://github.com/owner/repository/",
        "https://github.com:443/owner/repository",
    ],
)
def test_accepts_valid_github_urls(url: str) -> None:
    source = RepositorySourceFactory.create(url)

    assert isinstance(source, GitHubRepositorySource)


@pytest.mark.parametrize(
    "url",
    [
        "C:/Projects/private-repository",
        "/home/user/private-repository",
        "http://github.com/owner/repository",
        "https://github.com.evil.example/owner/repository",
        "https://evil-github.com/owner/repository",
        "https://user:password@github.com/owner/repository",
        "https://github.com/owner/repository?redirect=example.com",
        "https://github.com/owner",
        "https://github.com/owner/repository/extra",
        "https://github.com/../repository",
        "",
    ],
)
def test_rejects_invalid_repository_locations(url: str) -> None:
    with pytest.raises(ValueError):
        RepositorySourceFactory.create(url)
