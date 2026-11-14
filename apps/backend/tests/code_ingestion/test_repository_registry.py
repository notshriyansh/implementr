from pathlib import Path

import pytest

from app.repository_sources.repository_info import RepositoryInfo
from app.repository_sources.repository_registry import RepositoryRegistry


def make_repository_info(root: Path) -> RepositoryInfo:
    return RepositoryInfo(
        repository_id="test-repo-123",
        repository_name="test-repo",
        repository_root=root,
        branch="main",
        source="local",
        original_location=str(root),
    )


def test_register_and_get_repository(tmp_path: Path) -> None:
    registry = RepositoryRegistry()
    info = make_repository_info(tmp_path)

    registry.register(info)

    registered = registry.get("test-repo-123")

    assert registered is not None
    assert registered.repository_id == "test-repo-123"
    assert registered.repository_root == tmp_path.resolve()


def test_resolve_root_rejects_unknown_repository() -> None:
    registry = RepositoryRegistry()

    with pytest.raises(KeyError):
        registry.resolve_root("unknown-repo")


def test_resolve_file_returns_file_inside_repository(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    repository_root = tmp_path / "repository"
    repository_root.mkdir()

    source_file = repository_root / "main.py"
    source_file.write_text("print('hello')", encoding="utf-8")

    registry.register(make_repository_info(repository_root))

    resolved = registry.resolve_file("test-repo-123", "main.py")

    assert resolved == source_file.resolve()
    assert resolved.read_text(encoding="utf-8") == "print('hello')"


def test_resolve_file_rejects_parent_directory_traversal(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    repository_root = tmp_path / "repository"
    repository_root.mkdir()

    outside_file = tmp_path / "outside.py"
    outside_file.write_text("outside", encoding="utf-8")

    registry.register(make_repository_info(repository_root))

    with pytest.raises(ValueError, match="Invalid file path"):
        registry.resolve_file("test-repo-123", "../outside.py")


def test_resolve_file_rejects_absolute_path_outside_repository(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    repository_root = tmp_path / "repository"
    repository_root.mkdir()

    outside_file = tmp_path / "outside.py"
    outside_file.write_text("outside", encoding="utf-8")

    registry.register(make_repository_info(repository_root))

    with pytest.raises(ValueError, match="Invalid file path"):
        registry.resolve_file("test-repo-123", str(outside_file))


def test_resolve_file_rejects_symlink_escape(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    repository_root = tmp_path / "repository"
    repository_root.mkdir()

    outside_file = tmp_path / "outside.py"
    outside_file.write_text("outside", encoding="utf-8")

    link = repository_root / "linked.py"

    try:
        link.symlink_to(outside_file)
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation is unavailable in this environment")

    registry.register(make_repository_info(repository_root))

    with pytest.raises(ValueError, match="Invalid file path"):
        registry.resolve_file("test-repo-123", "linked.py")


def test_resolve_file_rejects_missing_file(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    registry.register(make_repository_info(tmp_path))

    with pytest.raises(FileNotFoundError):
        registry.resolve_file("test-repo-123", "missing.py")


def test_resolve_file_rejects_directory(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    subdirectory = tmp_path / "src"
    subdirectory.mkdir()

    registry.register(make_repository_info(tmp_path))

    with pytest.raises(FileNotFoundError):
        registry.resolve_file("test-repo-123", "src")


def test_resolve_root_rejects_repository_removed_after_registration(
    tmp_path: Path,
) -> None:
    registry = RepositoryRegistry()
    repository_root = tmp_path / "repository"
    repository_root.mkdir()

    registry.register(make_repository_info(repository_root))

    repository_root.rmdir()

    with pytest.raises(FileNotFoundError):
        registry.resolve_root("test-repo-123")