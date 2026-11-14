from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import (
    get_code_ingestion_service,
    get_repository_analyzer,
    get_repository_registry,
)
from app.main import app
from app.repository_sources.repository_info import RepositoryInfo
from app.repository_sources.repository_registry import RepositoryRegistry


@pytest.fixture
def registry(tmp_path):
    repository_root = tmp_path / "sample-repository"
    repository_root.mkdir()

    (repository_root / "main.py").write_text(
        "def main():\n    return 'hello'\n",
        encoding="utf-8",
    )

    ignored_dir = repository_root / "node_modules"
    ignored_dir.mkdir()
    (ignored_dir / "dependency.py").write_text(
        "SECRET = True\n",
        encoding="utf-8",
    )

    (repository_root / "README.md").write_text(
        "# Sample repository\n",
        encoding="utf-8",
    )

    outside_file = tmp_path / "outside.py"
    outside_file.write_text(
        "OUTSIDE_REPOSITORY = True\n",
        encoding="utf-8",
    )

    repository = RepositoryInfo(
        repository_id="test-repository",
        repository_name="sample-repository",
        repository_root=repository_root,
        branch="main",
        source="github",
        original_location="https://github.com/example/sample-repository",
    )

    result = RepositoryRegistry()
    result.register(repository)

    return {
        "registry": result,
        "root": repository_root,
        "outside_file": outside_file,
    }


@pytest.fixture
def client(registry):
    class FakeAnalyzer:
        def analyze(self, repo_path: str, repository_id: str):
            assert Path(repo_path) == registry["root"]
            assert repository_id == "test-repository"

            return SimpleNamespace(
                model_dump=lambda: {
                    "files": [
                        {
                            "path": "main.py",
                            "imports": [],
                            "functions": ["main"],
                            "classes": [],
                        }
                    ]
                }
            )

    app.dependency_overrides[get_repository_registry] = (
        lambda: registry["registry"]
    )
    app.dependency_overrides[get_repository_analyzer] = FakeAnalyzer

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_structure_returns_registered_repository(client):
    response = client.get(
        "/api/v1/repository/structure",
        params={"repository_id": "test-repository"},
    )

    assert response.status_code == 200
    assert response.json()["files"][0]["path"] == "main.py"


def test_structure_rejects_unknown_repository(client):
    response = client.get(
        "/api/v1/repository/structure",
        params={"repository_id": "unknown-repository"},
    )

    assert response.status_code == 404


def test_file_returns_source_content(client):
    response = client.get(
        "/api/v1/repository/file",
        params={
            "repository_id": "test-repository",
            "file_path": "main.py",
        },
    )

    assert response.status_code == 200
    assert "def main():" in response.json()["content"]
    assert response.json()["path"] == "main.py"
    assert response.json()["language"] == "python"


def test_file_rejects_path_traversal(client, registry):
    # Use a real file outside the registered repository so that
    # path resolution reaches the containment check.
    traversal = str(registry["outside_file"])

    response = client.get(
        "/api/v1/repository/file",
        params={
            "repository_id": "test-repository",
            "file_path": traversal,
        },
    )

    assert response.status_code == 400


def test_file_rejects_unknown_repository(client):
    response = client.get(
        "/api/v1/repository/file",
        params={
            "repository_id": "unknown-repository",
            "file_path": "main.py",
        },
    )

    assert response.status_code == 404


def test_file_rejects_missing_file(client):
    response = client.get(
        "/api/v1/repository/file",
        params={
            "repository_id": "test-repository",
            "file_path": "missing.py",
        },
    )

    assert response.status_code == 404


def test_file_rejects_ignored_directory(client):
    response = client.get(
        "/api/v1/repository/file",
        params={
            "repository_id": "test-repository",
            "file_path": "node_modules/dependency.py",
        },
    )

    assert response.status_code == 404


def test_file_rejects_unsupported_extension(client):
    response = client.get(
        "/api/v1/repository/file",
        params={
            "repository_id": "test-repository",
            "file_path": "README.md",
        },
    )

    assert response.status_code == 404


def test_ingestion_maps_invalid_url_to_400():
    class FakeIngestionService:
        repository_info = None

        async def ingest_repository(self, location):
            raise ValueError("Invalid GitHub repository URL")

    app.dependency_overrides[get_code_ingestion_service] = (
        lambda: FakeIngestionService()
    )

    try:
        with TestClient(app) as test_client:
            response = test_client.post(
                "/api/v1/repository/ingest",
                params={"location": "not-a-valid-url"},
            )

        assert response.status_code == 400
    finally:
        app.dependency_overrides.clear()


def test_ingestion_maps_git_failure_to_502():
    class FakeIngestionService:
        repository_info = None

        async def ingest_repository(self, location):
            raise RuntimeError("Internal git stderr should not be exposed")

    app.dependency_overrides[get_code_ingestion_service] = (
        lambda: FakeIngestionService()
    )

    try:
        with TestClient(app) as test_client:
            response = test_client.post(
                "/api/v1/repository/ingest",
                params={"location": "https://github.com/example/repository"},
            )

        assert response.status_code == 502
        assert response.json()["detail"] == (
            "Unable to fetch the GitHub repository."
        )
        assert "Internal git stderr" not in response.text
    finally:
        app.dependency_overrides.clear()


def test_ingestion_returns_registered_repository_identity():
    repository_root = Path("data/repositories/test-repository")

    repository = RepositoryInfo(
        repository_id="test-repository",
        repository_name="sample-repository",
        repository_root=repository_root,
        branch="main",
        source="github",
        original_location="https://github.com/example/sample-repository",
    )

    class FakeIngestionService:
        repository_info = None

        async def ingest_repository(self, location):
            assert location == "https://github.com/example/sample-repository"
            self.repository_info = repository
            return []

    app.dependency_overrides[get_code_ingestion_service] = (
        lambda: FakeIngestionService()
    )

    try:
        with TestClient(app) as test_client:
            response = test_client.post(
                "/api/v1/repository/ingest",
                params={
                    "location": " https://github.com/example/sample-repository "
                },
            )

        assert response.status_code == 200
        assert response.json()["repository_id"] == "test-repository"
        assert response.json()["repository"] == "sample-repository"
    finally:
        app.dependency_overrides.clear()
