from pydantic import BaseModel


class CodeChunk(BaseModel):
    chunk_id: str

    repository_id: str

    repository_name: str

    relative_path: str

    source: str

    branch: str = "main"

    language: str

    content: str

    start_line: int

    end_line: int