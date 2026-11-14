from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import asyncio

from app.reproduction.research_reproduction_service import (
    ResearchReproductionService,
)


def test_generate_scopes_repository_retrieval():
    repository_id = "repo-123"

    paper_chunks = [
        SimpleNamespace(text="A paper about transformers.")
    ]
    code_chunks = [
        SimpleNamespace(
            relative_path="src/model.py",
            content="class Model: pass",
        )
    ]
    symbols = [
        SimpleNamespace(
            symbol_name="Model",
            symbol_type="class",
            relative_path="src/model.py",
            code="class Model: pass",
        )
    ]

    retrieval = MagicMock()
    retrieval.retrieve = AsyncMock(return_value=paper_chunks)

    code_retrieval = MagicMock()
    code_retrieval.retrieve = AsyncMock(return_value=code_chunks)

    symbol_retrieval = MagicMock()
    symbol_retrieval.retrieve = AsyncMock(return_value=symbols)

    architecture = MagicMock()
    architecture.analyze = AsyncMock(
        return_value=SimpleNamespace(reasoning="Architecture context")
    )

    concept_service = MagicMock()
    concept_service.build_concept_map = AsyncMock(
        return_value={
            "paper_concepts": [
                SimpleNamespace(name="Transformer")
            ],
            "repository_concepts": [
                SimpleNamespace(name="Model")
            ],
            "matches": [
                SimpleNamespace(
                    paper_concept="Transformer",
                    repository_concept="Model",
                    similarity=0.9,
                )
            ],
        }
    )

    gap_analyzer = MagicMock()
    gap_analyzer.analyze.return_value = []

    llm = MagicMock()
    llm.generate = AsyncMock(
        return_value=(
            "PAPER_SUMMARY: Summary\n"
            "REPOSITORY_TARGETS:\n- src/model.py\n"
            "CONCEPT_MAPPINGS:\n- Transformer -> Model\n"
            "ARCHITECTURE_GAPS:\n"
            "IMPLEMENTATION_STEPS:\n- Update model\n"
            "MODIFICATION_TARGETS:\n- src/model.py\n"
            "GAP_TO_SYMBOL_MAPPING:\n- Transformer -> Model\n"
            "REQUIRED_CHANGES:\n- Change model\n"
            "TRAINING_CHANGES:\n"
            "EVALUATION_CHANGES:\n"
            "BENCHMARK_TASKS:\n"
            "SUCCESS_CRITERIA:\n"
            "RISKS:\n- Regression risk\n"
        )
    )

    cache = MagicMock()
    cache.get.return_value = None

    service = ResearchReproductionService(
        retrieval_service=retrieval,
        code_retrieval_service=code_retrieval,
        symbol_retrieval_service=symbol_retrieval,
        architecture_service=architecture,
        concept_service=concept_service,
        gap_analyzer=gap_analyzer,
        llm=llm,
        cache=cache,
    )

    asyncio.run(
        service.generate(
            "How can this paper be implemented?",
            repository_id=repository_id,
        )
    )

    code_retrieval.retrieve.assert_awaited_once_with(
        query="How can this paper be implemented?",
        k=5,
        repository_id=repository_id,
    )

    symbol_retrieval.retrieve.assert_awaited_once_with(
        query="How can this paper be implemented?",
        k=25,
        repository_id=repository_id,
    )

    architecture.analyze.assert_awaited_once_with(
        "How can this paper be implemented?",
        repository_id=repository_id,
    )