from unittest.mock import AsyncMock, MagicMock

import asyncio

from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)


def test_analyze_scopes_retrieval_and_cache_by_repository():
    code_retrieval = MagicMock()
    code_retrieval.retrieve = AsyncMock(return_value=[])

    symbol_retrieval = MagicMock()
    symbol_retrieval.retrieve = AsyncMock(return_value=[])

    execution_flow = MagicMock()
    execution_flow.expand_query = AsyncMock(
        return_value={
            "symbols": [],
            "execution_paths": [],
        }
    )

    context_expander = MagicMock()
    context_expander.expand.return_value = []

    llm = MagicMock()
    llm.generate = AsyncMock(
        return_value="SUMMARY: Example architecture summary"
    )

    cache = MagicMock()
    cache.get.return_value = None

    service = ArchitectureReasoningService(
        code_retrieval_service=code_retrieval,
        symbol_retrieval_service=symbol_retrieval,
        execution_flow_service=execution_flow,
        context_expander=context_expander,
        llm=llm,
        cache=cache,
    )

    query = "Explain the model architecture"

    asyncio.run(
        service.analyze(query, repository_id="repo-A")
    )

    asyncio.run(
        service.analyze(query, repository_id="repo-B")
    )

    assert code_retrieval.retrieve.await_args_list[0].kwargs == {
        "query": query,
        "k": 5,
        "repository_id": "repo-A",
    }
    assert code_retrieval.retrieve.await_args_list[1].kwargs == {
        "query": query,
        "k": 5,
        "repository_id": "repo-B",
    }

    assert symbol_retrieval.retrieve.await_args_list[0].kwargs == {
        "query": query,
        "k": 5,
        "repository_id": "repo-A",
    }
    assert symbol_retrieval.retrieve.await_args_list[1].kwargs == {
        "query": query,
        "k": 5,
        "repository_id": "repo-B",
    }

    cache_keys = [
        call.args[0]
        for call in cache.get.call_args_list
    ]

    assert cache_keys == [
        f"architecture:repo-A:{query}",
        f"architecture:repo-B:{query}",
    ]