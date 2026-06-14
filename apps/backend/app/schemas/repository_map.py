from pydantic import BaseModel


class FileNode(BaseModel):
    path: str
    imports: list[str]
    functions: list[str]
    classes: list[str]


class RepositoryMap(BaseModel):
    files: list[FileNode]