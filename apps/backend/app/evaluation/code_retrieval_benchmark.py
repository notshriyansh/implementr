from statistics import fmean
from time import perf_counter
from typing import Any

import numpy as np

from app.evaluation.code_retrieval_dataset import (
    CodeRetrievalBenchmarkCase,
)
from app.evaluation.metrics import evaluate_ranking


def normalize_relative_path(path: str) -> str:
    return path.replace("\\", "/").removeprefix("./")


async def evaluate_code_retrieval(
    retrieval_service: Any,
    cases: tuple[CodeRetrievalBenchmarkCase, ...],
    repository_id: str,
    k: int = 5,
) -> list[dict[str, Any]]:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")

    if not cases:
        raise ValueError("At least one benchmark case is required")

    results: list[dict[str, Any]] = []

    for case in cases:
        if not case.expected_files:
            raise ValueError(
                f"Benchmark case {case.case_id!r} has no relevant files"
            )

        expected_files = [
            normalize_relative_path(path)
            for path in case.expected_files
        ]

        started = perf_counter()
        chunks = await retrieval_service.retrieve(
            query=case.question,
            k=k,
            repository_id=repository_id,
        )
        latency_ms = (perf_counter() - started) * 1000

        retrieved_files = [
            normalize_relative_path(chunk.relative_path)
            for chunk in chunks
        ]

        metrics = evaluate_ranking(
            retrieved_ids=retrieved_files,
            relevant_ids=set(expected_files),
            k=k,
        )

        results.append(
            {
                "case_id": case.case_id,
                "question": case.question,
                "expected_files": expected_files,
                "retrieved_files": retrieved_files,
                "latency_ms": latency_ms,
                **metrics,
            }
        )

    return results


def summarize_code_retrieval_results(
    results: list[dict[str, Any]],
    k: int = 5,
) -> dict[str, Any]:
    if not results:
        raise ValueError("Cannot summarize an empty result set")

    metric_names = (
        f"recall@{k}",
        f"precision@{k}",
        "reciprocal_rank",
        f"ndcg@{k}",
    )

    summary: dict[str, Any] = {
        "case_count": len(results),
        "k": k,
    }

    for name in metric_names:
        summary[f"mean_{name}"] = fmean(
            float(result[name]) for result in results
        )

    latencies = np.asarray(
        [float(result["latency_ms"]) for result in results],
        dtype=np.float64,
    )

    summary["mean_latency_ms"] = float(np.mean(latencies))
    summary["p50_latency_ms"] = float(np.percentile(latencies, 50))
    summary["p95_latency_ms"] = float(np.percentile(latencies, 95))

    return summary
