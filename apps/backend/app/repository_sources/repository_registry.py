
from pathlib import Path
from threading import RLock

from app.repository_sources.repository_info import RepositoryInfo


class RepositoryRegistry:
    """Stores trusted metadata for repositories prepared by this application."""

    def __init__(self) -> None:
        self._repositories: dict[str, RepositoryInfo] = {}
        self._lock = RLock()

    def register(self, repository: RepositoryInfo) -> None:
        root = repository.repository_root.resolve(strict=True)

        if not root.is_dir():
            raise ValueError("Repository root must be a directory")

        registered = RepositoryInfo(
            repository_id=repository.repository_id,
            repository_name=repository.repository_name,
            repository_root=root,
            branch=repository.branch,
            source=repository.source,
            original_location=repository.original_location,
        )

        with self._lock:
            self._repositories[repository.repository_id] = registered

    def get(self, repository_id: str) -> RepositoryInfo | None:
        with self._lock:
            return self._repositories.get(repository_id)

    def resolve_root(self, repository_id: str) -> Path:
        repository = self.get(repository_id)

        if repository is None:
            raise KeyError(repository_id)

        root = repository.repository_root.resolve(strict=True)

        if not root.is_dir():
            raise FileNotFoundError(root)

        return root

    def resolve_file_with_root(
        self,
        repository_id: str,
        file_path: str,
    ) -> tuple[Path, Path]:
        root = self.resolve_root(repository_id)

        target = (root / file_path).resolve(strict=True)

        try:
            target.relative_to(root)
        except ValueError as exc:
            raise ValueError("Invalid file path") from exc

        if not target.is_file():
            raise FileNotFoundError(target)

        return root, target


    def resolve_file(
        self,
        repository_id: str,
        file_path: str,
    ) -> Path:
        _, target = self.resolve_file_with_root(
            repository_id,
            file_path,
        )
        return target
