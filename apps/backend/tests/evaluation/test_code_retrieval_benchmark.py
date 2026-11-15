
import asyncio

import pytest

from app.evaluation.code_retrieval_benchmark import (
    evaluate_code_retrieval,
    normalize_relative_path,
    summarize_code_retrieval_results,
)
from app.evaluation.code_retrieval_dataset import (
    CodeRetrievalBenchmarkCase,
)
from app.schemas.code_chunk import CodeChunk


def make_chunk(path: str) -> CodeChunk:
    return CodeChunk(
        chunk_id=f"chunk-{path}",
        repository_id="test-repository",
        repository_name="test-repository",
        relative_path=path,
        source="repository",
        language=".py",
        content="def example(): pass",
        start_line=1,
        end_line=1,
    )


class FakeRetrievalService:
    def __init__(self, results_by_query):
        self.results_by_query = results_by_query
        self.calls = []

    async def retrieve(self, query, k=5, repository_id=None):
        self.calls.append(
            {
                "query": query,
                "k": k,
                "repository_id": repository_id,
            }
        )
        return self.results_by_query[query][:k]


def test_normalize_relative_path():
    assert normalize_relative_path(
        r".\app\code_retrieval\retrieval_utils.py"
    ) == "app/code_retrieval/retrieval_utils.py"


def test_evaluation_uses_real_retrieval_interface_and_existing_metrics():
    case = CodeRetrievalBenchmarkCase(
        case_id="retrieval-test-001",
        question="How are code files deduplicated?",
        expected_files=(
            "app/code_retrieval/retrieval_utils.py",
        ),
    )

    service = FakeRetrievalService(
        {
            case.question: [
                make_chunk("app\\code_retrieval\\retrieval_utils.py"),
                make_chunk("app/other.py"),
            ]
        }
    )

    results = asyncio.run(
        evaluate_code_retrieval(
            retrieval_service=service,
            cases=(case,),
            repository_id="test-repository",
            k=2,
        )
    )

    assert len(results) == 1
    result = results[0]

    assert result["case_id"] == case.case_id
    assert result["retrieved_files"] == [
        "app/code_retrieval/retrieval_utils.py",
        "app/other.py",
    ]
    assert result["recall@2"] == 1.0
    assert result["precision@2"] == 0.5
    assert result["reciprocal_rank"] == 1.0
    assert result["ndcg@2"] == 1.0
    assert result["latency_ms"] >= 0

    assert service.calls == [
        {
            "query": case.question,
            "k": 2,
            "repository_id": "test-repository",
        }
    ]


def test_evaluation_rejects_invalid_k():
    service = FakeRetrievalService({})
    case = CodeRetrievalBenchmarkCase(
        case_id="invalid-k",
        question="Any question",
        expected_files=("app/example.py",),
    )

    for invalid_k in (0, -1, True, 1.5):
        with pytest.raises(ValueError, match="positive integer"):
            asyncio.run(
                evaluate_code_retrieval(
                    retrieval_service=service,
                    cases=(case,),
                    repository_id="test-repository",
                    k=invalid_k,
                )
            )


def test_evaluation_rejects_empty_dataset():
    with pytest.raises(ValueError, match="At least one"):
        asyncio.run(
            evaluate_code_retrieval(
                retrieval_service=FakeRetrievalService({}),
                cases=(),
                repository_id="test-repository",
            )
        )


def test_summary_averages_metrics_and_calculates_latency_percentiles():
    results = [
        {
            "recall@2": 1.0,
            "precision@2": 0.5,
            "reciprocal_rank": 1.0,
            "ndcg@2": 1.0,
            "latency_ms": 10.0,
        },
        {
            "recall@2": 0.0,
            "precision@2": 0.0,
            "reciprocal_rank": 0.0,
            "ndcg@2": 0.0,
            "latency_ms": 30.0,
        },
    ]

    summary = summarize_code_retrieval_results(results, k=2)

    assert summary["case_count"] == 2
    assert summary["k"] == 2
    assert summary["mean_recall@2"] == 0.5
    assert summary["mean_precision@2"] == 0.25
    assert summary["mean_reciprocal_rank"] == 0.5
    assert summary["mean_ndcg@2"] == 0.5
    assert summary["mean_latency_ms"] == 20.0
    assert summary["p50_latency_ms"] == 20.0
    assert summary["p95_latency_ms"] == pytest.approx(29.0)
