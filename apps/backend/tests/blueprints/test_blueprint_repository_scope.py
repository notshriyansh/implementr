from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import asyncio

from app.blueprints.implementation_blueprint_service import (
    ImplementationBlueprintService,
)


def test_generate_forwards_repository_id():
    repository_id = "repo-123"

    plan = SimpleNamespace(
        paper_summary="Paper summary",
        modification_targets=["src/model.py"],
        gap_to_symbol_mapping=["Transformer -> Model"],
        risks=["Regression risk"],
    )

    reproduction_service = MagicMock()
    reproduction_service.generate = AsyncMock(return_value=plan)

    symbols = [
        SimpleNamespace(
            symbol_name="Model",
            relative_path="src/model.py",
            symbol_type="class",
            code="class Model: pass",
        )
    ]

    symbol_retrieval = MagicMock()
    symbol_retrieval.retrieve = AsyncMock(return_value=symbols)

    llm = MagicMock()
    llm.generate = AsyncMock(
        return_value=(
            '{"blueprint_steps": [{'
            '"file_path": "src/model.py",'
            '"symbol_name": "Model",'
            '"change_type": "modify",'
            '"reason": "Adapt model",'
            '"implementation_steps": ["Update forward"],'
            '"validation_steps": ["Run tests"],'
            '"expected_outcome": "Updated model"'
            '}]}'
        )
    )

    service = ImplementationBlueprintService(
        reproduction_service=reproduction_service,
        symbol_retrieval_service=symbol_retrieval,
        llm=llm,
    )

    asyncio.run(
        service.generate(
            "Implement the paper",
            repository_id=repository_id,
        )
    )

    reproduction_service.generate.assert_awaited_once_with(
        "Implement the paper",
        repository_id=repository_id,
    )

    symbol_retrieval.retrieve.assert_awaited_once_with(
        query="Implement the paper",
        k=10,
        repository_id=repository_id,
    )