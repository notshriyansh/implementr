import hashlib
import shutil

from pathlib import Path

from app.repository_sources.base import (
    RepositorySource,
)

from app.repository_sources.git import (
    GitClient,
)

from app.repository_sources.repository_info import (
    RepositoryInfo,
)


CACHE_DIR = Path(
    "data/repositories"
)


class GitHubRepositorySource(
    RepositorySource
):

    def __init__(self) -> None:
        self.git = GitClient()

    async def prepare(
        self,
        location: str,
    ) -> RepositoryInfo:

        repository_id = hashlib.sha256(
            location.encode()
        ).hexdigest()[:16]

        repository_root = (
            CACHE_DIR / repository_id
        )

        CACHE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        git_dir = (
            repository_root
            / ".git"
        )

        if git_dir.exists():

            try:
                self.git.pull(
                    repository_root
                )

            except Exception:

                shutil.rmtree(
                    repository_root
                )

                self.git.clone(
                    repository_url=location,
                    destination=repository_root,
                )

        else:

            if repository_root.exists():
                shutil.rmtree(
                    repository_root
                )

            self.git.clone(
                repository_url=location,
                destination=repository_root,
            )

        branch = (
            self.git.current_branch(
                repository_root
            )
        )

        repository_name = (
            location.rstrip("/")
            .split("/")[-1]
            .removesuffix(".git")
        )

        return RepositoryInfo(
            repository_id=repository_id,
            repository_name=repository_name,
            repository_root=repository_root,
            branch=branch,
            source="github",
            original_location=location,
        )

    async def cleanup(
        self,
    ) -> None:
        return