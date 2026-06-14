from pydantic import BaseModel


class CodeChunk(BaseModel):
    chunk_id: str

    file_path: str

    language: str

    content: str

    start_line: int

    end_line: int