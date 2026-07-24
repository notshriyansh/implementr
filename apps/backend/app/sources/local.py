from pathlib import Path


from app.sources.base import (
    BaseRepositorySource,
)


from app.sources.models import (
    LocalRepositoryModel,
)



class LocalRepositorySource(
    BaseRepositorySource,
):
    source: LocalRepositoryModel

    def __init__(
        self,
        source: LocalRepositoryModel,
    ):
        self.source = source

    async def prepare(
        self,
    ) -> Path:

        path = Path(
            self.source.path
        )

        if not path.exists():
            raise FileNotFoundError(
                path
            )

        if not path.is_dir():
            raise NotADirectoryError(
                path
            )

        return path