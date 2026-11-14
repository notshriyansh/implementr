from pathlib import Path

import pytest

from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)
from app.code_ingestion.repository_analyzer import (
    RepositoryAnalyzer,
)


class TestScanner:
    def scan(self, repo_path: str) -> list[Path]:
        return list(Path(repo_path).rglob("*.py"))


def create_repository(
    root: Path,
    import_name: str,
) -> None:
    root.mkdir(parents=True, exist_ok=True)

    (root / "model.py").write_text(
        f"""
import {import_name}

class Model:
    def predict(self):
        self.normalize()

    def normalize(self):
        pass
""",
        encoding="utf-8",
    )


def test_analyzer_isolates_repositories_and_preserves_previous_graph(
    tmp_path,
):
    registry = RepositoryGraphRegistry()

    analyzer = RepositoryAnalyzer(
        graph_registry=registry,
        scanner=TestScanner(),
    )

    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"

    create_repository(repo_a, "numpy")
    create_repository(repo_b, "torch")

    # Ingest A.
    analyzer.analyze(
        repo_path=str(repo_a),
        repository_id="repo-A",
    )

    graph_a = registry.get("repo-A")

    assert graph_a is not None
    assert graph_a.get_related_files("model.py") == ["numpy"]

    # Ingest B.
    analyzer.analyze(
        repo_path=str(repo_b),
        repository_id="repo-B",
    )

    graph_b = registry.get("repo-B")

    assert graph_b is not None
    assert graph_b.get_related_files("model.py") == ["torch"]

    # A must remain unchanged.
    assert registry.get("repo-A") is graph_a
    assert graph_a.get_related_files("model.py") == ["numpy"]

    # Re-ingest A with different contents.
    create_repository(repo_a, "pandas")

    analyzer.analyze(
        repo_path=str(repo_a),
        repository_id="repo-A",
    )

    updated_graph_a = registry.get("repo-A")

    assert updated_graph_a is not graph_a
    assert updated_graph_a.get_related_files("model.py") == ["pandas"]

    # Updating A must not affect B.
    assert registry.get("repo-B") is graph_b
    assert graph_b.get_related_files("model.py") == ["torch"]

def test_failed_analysis_preserves_previous_graph(tmp_path):
    registry = RepositoryGraphRegistry()

    analyzer = RepositoryAnalyzer(
        graph_registry=registry,
        scanner=TestScanner(),
    )

    repo = tmp_path / "repo"
    create_repository(repo, "numpy")

    analyzer.analyze(
        repo_path=str(repo),
        repository_id="repo-A",
    )

    previous_graph = registry.get("repo-A")

    class FailingScanner:
        def scan(self, repo_path: str):
            raise RuntimeError("Scanner failed")

    failing_analyzer = RepositoryAnalyzer(
        graph_registry=registry,
        scanner=FailingScanner(),
    )

    with pytest.raises(RuntimeError):
        failing_analyzer.analyze(
            repo_path=str(repo),
            repository_id="repo-A",
        )

    assert registry.get("repo-A") is previous_graph