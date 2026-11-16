from app.architecture.repository_graph import RepositoryGraph
from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)
from app.architecture.context_expander import ContextExpander


def test_context_expander_uses_only_selected_repository():
    registry = RepositoryGraphRegistry()

    graph_a = RepositoryGraph()
    graph_a.add_file("model.py", ["numpy_utils.py"])

    graph_b = RepositoryGraph()
    graph_b.add_file("model.py", ["torch_utils.py"])

    registry.replace("repo-A", graph_a)
    registry.replace("repo-B", graph_b)

    expander = ContextExpander(
        graph_registry=registry,
    )

    result_a = expander.expand(
        ["model.py"],
        repository_id="repo-A",
    )

    result_b = expander.expand(
        ["model.py"],
        repository_id="repo-B",
    )

    assert set(result_a) == {
        "model.py",
        "numpy_utils.py",
    }

    assert set(result_b) == {
        "model.py",
        "torch_utils.py",
    }


def test_unknown_repository_does_not_fall_back_to_another_graph():
    registry = RepositoryGraphRegistry()

    graph = RepositoryGraph()
    graph.add_file("model.py", ["private_utils.py"])

    registry.replace("repo-A", graph)

    expander = ContextExpander(
        graph_registry=registry,
    )

    result = expander.expand(
        ["model.py"],
        repository_id="unknown-repo",
    )

    assert result == ["model.py"]