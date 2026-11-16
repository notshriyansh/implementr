from app.architecture.repository_graph import RepositoryGraph
from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)


def test_graphs_are_isolated_by_repository():
    registry = RepositoryGraphRegistry()

    graph_a = RepositoryGraph()
    graph_a.add_symbol("Model", "src/model.py")

    graph_b = RepositoryGraph()
    graph_b.add_symbol("Model", "backend/model.py")

    registry.replace("repo-A", graph_a)
    registry.replace("repo-B", graph_b)

    assert (
        registry.get("repo-A").get_symbol_file("Model")
        == "src/model.py"
    )
    assert (
        registry.get("repo-B").get_symbol_file("Model")
        == "backend/model.py"
    )


def test_replacing_one_graph_does_not_change_another():
    registry = RepositoryGraphRegistry()

    graph_a = RepositoryGraph()
    graph_a.add_file("src/model.py", ["src/utils.py"])

    graph_b = RepositoryGraph()
    graph_b.add_file("src/model.py", ["src/database.py"])

    registry.replace("repo-A", graph_a)
    registry.replace("repo-B", graph_b)

    replacement_a = RepositoryGraph()
    replacement_a.add_file("src/model.py", ["src/new_utils.py"])

    registry.replace("repo-A", replacement_a)

    assert (
        registry.get("repo-A").get_related_files("src/model.py")
        == ["src/new_utils.py"]
    )
    assert (
        registry.get("repo-B").get_related_files("src/model.py")
        == ["src/database.py"]
    )


def test_unknown_repository_returns_none():
    registry = RepositoryGraphRegistry()

    assert registry.get("unknown-repo") is None


def test_removing_repository_does_not_remove_other_graphs():
    registry = RepositoryGraphRegistry()

    graph_a = RepositoryGraph()
    graph_b = RepositoryGraph()

    registry.replace("repo-A", graph_a)
    registry.replace("repo-B", graph_b)

    assert registry.remove("repo-A") is True
    assert registry.get("repo-A") is None
    assert registry.get("repo-B") is graph_b
