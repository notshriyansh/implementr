import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.architecture.repository_graph import RepositoryGraph
from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)
from app.architecture.execution_flow_service import (
    ExecutionFlowService,
)


def test_execution_flow_uses_selected_repository_graph():
    registry = RepositoryGraphRegistry()

    graph_a = RepositoryGraph()
    graph_a.add_file("model.py", ["numpy"])
    graph_a.add_symbol("Model", "model.py")
    graph_a.add_call("Model", "predict")

    graph_b = RepositoryGraph()
    graph_b.add_file("model.py", ["torch"])
    graph_b.add_symbol("Model", "model.py")
    graph_b.add_call("Model", "forward")

    registry.replace("repo-A", graph_a)
    registry.replace("repo-B", graph_b)

    symbol_service = AsyncMock()
    symbol_service.retrieve.return_value = [
        SimpleNamespace(
            symbol_name="Model",
            relative_path="model.py",
        )
    ]

    service = ExecutionFlowService(
        graph_registry=registry,
        symbol_service=symbol_service,
    )

    result_a = asyncio.run(
        service.expand_query(
            query="model architecture",
            repository_id="repo-A",
        )
    )

    result_b = asyncio.run(
        service.expand_query(
            query="model architecture",
            repository_id="repo-B",
        )
    )

    assert result_a["symbols"][0]["imports"] == ["numpy"]
    assert result_a["symbols"][0]["calls"] == ["predict"]

    assert result_b["symbols"][0]["imports"] == ["torch"]
    assert result_b["symbols"][0]["calls"] == ["forward"]

    assert symbol_service.retrieve.await_count == 2

    for call in symbol_service.retrieve.await_args_list:
        assert call.kwargs["k"] == 5

    assert [
        call.kwargs["repository_id"]
        for call in symbol_service.retrieve.await_args_list
    ] == ["repo-A", "repo-B"]