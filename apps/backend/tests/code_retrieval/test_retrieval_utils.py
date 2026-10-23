
from app.code_retrieval.retrieval_utils import deduplicate_files
from app.schemas.code_chunk import CodeChunk


def make_chunk(
    *,
    chunk_id: str,
    repository_id: str,
    relative_path: str,
    content: str,
) -> CodeChunk:
    return CodeChunk(
        chunk_id=chunk_id,
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path=relative_path,
        source="repository",
        language=".py",
        content=content,
        start_line=1,
        end_line=10,
    )


def test_deduplicate_files_keeps_first_chunk_per_file() -> None:
    first = make_chunk(
        chunk_id="chunk-1",
        repository_id="repo-a",
        relative_path="src/main.py",
        content="first result",
    )
    duplicate = make_chunk(
        chunk_id="chunk-2",
        repository_id="repo-a",
        relative_path="src/main.py",
        content="duplicate result",
    )
    another_file = make_chunk(
        chunk_id="chunk-3",
        repository_id="repo-a",
        relative_path="src/utils.py",
        content="another file",
    )

    results = deduplicate_files(
        [first, duplicate, another_file]
    )

    assert [chunk.chunk_id for chunk in results] == [
        "chunk-1",
        "chunk-3",
    ]


def test_deduplicate_files_keeps_same_path_from_different_repositories() -> None:
    repo_a_chunk = make_chunk(
        chunk_id="chunk-a",
        repository_id="repo-a",
        relative_path="src/main.py",
        content="repository A implementation",
    )
    repo_b_chunk = make_chunk(
        chunk_id="chunk-b",
        repository_id="repo-b",
        relative_path="src/main.py",
        content="repository B implementation",
    )

    results = deduplicate_files(
        [repo_a_chunk, repo_b_chunk]
    )

    assert [chunk.chunk_id for chunk in results] == [
        "chunk-a",
        "chunk-b",
    ]
