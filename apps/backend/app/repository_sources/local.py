import hashlib
from pathlib import Path

from app.repository_sources.base import (
    RepositorySource,
)

from app.repository_sources.repository_info import (
    RepositoryInfo,
)


class LocalRepositorySource(
    RepositorySource
):

    async def prepare(
        self,
        location: str,
    ) -> RepositoryInfo:

        root = Path(location).resolve()

        repository_name = root.name

        repository_id = hashlib.sha256(
            str(root).encode()
        ).hexdigest()[:16]

        return RepositoryInfo(
            repository_id=repository_id,
            repository_name=repository_name,
            repository_root=root,
            branch="main",
            source="local",
            original_location=location,
        )