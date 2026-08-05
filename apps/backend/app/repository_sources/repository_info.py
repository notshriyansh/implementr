from pathlib import Path

from pydantic import BaseModel


class RepositoryInfo(BaseModel):
    repository_id: str

    repository_name: str

    repository_root: Path

    branch: str = "main"

    source: str

    original_location: str