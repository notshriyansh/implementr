import argparse
import asyncio
import csv
import math
import statistics
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

from app.code_vectorstores.symbol_vector_store import SymbolVectorStore
from app.schemas.code_symbol import CodeSymbol


def normalize_rows(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.maximum(norms, 1e-12)


def make_symbol(
    index: int,
    repository_id: str,
) -> CodeSymbol:
    return CodeSymbol(
        symbol_id=f"symbol-{index:08d}",
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path=f"src/module_{index}.py",
        symbol_name=f"function_{index}",
        symbol_type="function",
        code=f"def function_{index}(): pass",
        start_line=1,
        end_line=1,
        importance=1,
    )


def make_dataset(
    size: int,
    dimension: int,
    query_count: int,
    repository_count: int,
    relevant_per_query: int,
    hard_negatives_per_query: int,
    seed: int,
):
    """Create random background symbols plus known relevant symbols.

    Relevant symbols are close to each query and belong to its target
    repository. Hard negatives are even closer to the query but belong
    to a different repository, creating a repository-filtering stress test.
    """
    required = query_count * (
        relevant_per_query + hard_negatives_per_query
    )
    if size < required:
        raise ValueError(
            f"Index size {size} is too small; need at least {required}."
        )

    rng = np.random.default_rng(seed)

    queries = normalize_rows(
        rng.normal(size=(query_count, dimension)).astype(np.float32)
    )

    vectors = rng.normal(size=(size, dimension)).astype(np.float32)
    repositories = [
        f"repo-{int(i)}"
        for i in rng.integers(0, repository_count, size=size)
    ]

    relevant_ids: list[set[str]] = []
    target_repositories: list[str] = []

    cursor = 0

    for query_index, query in enumerate(queries):
        target = f"repo-{query_index % repository_count}"
        distractor = f"repo-{(query_index + 1) % repository_count}"

        target_repositories.append(target)
        current_relevant: set[str] = set()

        for _ in range(relevant_per_query):
            vectors[cursor] = query + rng.normal(
                scale=0.08,
                size=dimension,
            )
            repositories[cursor] = target
            current_relevant.add(f"symbol-{cursor:08d}")
            cursor += 1

        for _ in range(hard_negatives_per_query):
            vectors[cursor] = query + rng.normal(
                scale=0.02,
                size=dimension,
            )
            repositories[cursor] = distractor
            cursor += 1

        relevant_ids.append(current_relevant)

    vectors = normalize_rows(vectors)

    symbols = [
        make_symbol(index, repositories[index])
        for index in range(size)
    ]

    return vectors, symbols, queries, target_repositories, relevant_ids


def ranking_metrics(
    result_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> dict[str, float]:
    ranked = result_ids[:k]
    hits = [1 if symbol_id in relevant_ids else 0 for symbol_id in ranked]

    recall = sum(hits) / max(len(relevant_ids), 1)
    precision = sum(hits) / k

    reciprocal_rank = 0.0
    for rank, hit in enumerate(hits, start=1):
        if hit:
            reciprocal_rank = 1.0 / rank
            break

    dcg = sum(
        hit / math.log2(rank + 1)
        for rank, hit in enumerate(hits, start=1)
    )

    ideal_hits = min(len(relevant_ids), k)
    idcg = sum(
        1.0 / math.log2(rank + 1)
        for rank in range(1, ideal_hits + 1)
    )

    return {
        f"recall@{k}": recall,
        f"precision@{k}": precision,
        "mrr": reciprocal_rank,
        f"ndcg@{k}": dcg / idcg if idcg else 0.0,
    }


def percentile(values: list[float], p: float) -> float:
    return float(np.percentile(values, p))


def estimate_metadata_bytes(symbols: list[CodeSymbol]) -> int:
    """Approximate Python-side metadata size, not total process RSS."""
    total = sys.getsizeof(symbols)

    for symbol in symbols:
        total += sys.getsizeof(symbol)
        total += sys.getsizeof(symbol.__dict__)

        for value in symbol.__dict__.values():
            total += sys.getsizeof(value)

    return total


def benchmark_size(
    size: int,
    args: argparse.Namespace,
    temp_dir: Path,
    loop: asyncio.AbstractEventLoop,
) -> list[dict]:
    (
        vectors,
        symbols,
        queries,
        target_repositories,
        relevant_ids,
    ) = make_dataset(
        size=size,
        dimension=args.dimension,
        query_count=args.queries,
        repository_count=args.repositories,
        relevant_per_query=args.relevant_per_query,
        hard_negatives_per_query=args.hard_negatives_per_query,
        seed=args.seed + size,
    )

    SymbolVectorStore.INDEX_PATH = temp_dir / f"symbols-{size}.index"
    SymbolVectorStore.METADATA_PATH = temp_dir / f"symbols-{size}.json"

    store = SymbolVectorStore(embedding_dimension=args.dimension)
    loop.run_until_complete(store.add_symbols(vectors, symbols))

    quality_results = {"global": [], "scoped": []}

    for query_index, query in enumerate(queries):
        query_embedding = query.reshape(1, -1).copy()

        global_results = loop.run_until_complete(
            store.similarity_search(
                query_embedding.copy(),
                k=args.k,
            )
        )

        scoped_results = loop.run_until_complete(
            store.similarity_search(
                query_embedding.copy(),
                k=args.k,
                repository_id=target_repositories[query_index],
            )
        )
        scoped_candidate_count = statistics.mean(
            sum(
                symbol.repository_id == repository_id
                for symbol in symbols
            )
            for repository_id in target_repositories
        )

        quality_results["global"].append(
            ranking_metrics(
                [symbol.symbol_id for symbol in global_results],
                relevant_ids[query_index],
                args.k,
            )
        )
        quality_results["scoped"].append(
            ranking_metrics(
                [symbol.symbol_id for symbol in scoped_results],
                relevant_ids[query_index],
                args.k,
            )
        )

    for query_index in range(min(args.queries, args.warmups)):
        query_embedding = queries[query_index].reshape(1, -1).copy()

        loop.run_until_complete(
            store.similarity_search(query_embedding.copy(), k=args.k)
        )
        loop.run_until_complete(
            store.similarity_search(
                query_embedding.copy(),
                k=args.k,
                repository_id=target_repositories[query_index],
            )
        )

    latency_ms = {"global": [], "scoped": []}

    # Alternate call order to reduce systematic ordering bias.
    for repeat in range(args.repeats):
        for query_index, query in enumerate(queries):
            query_embedding = query.reshape(1, -1).copy()

            modes = ["global", "scoped"]
            if (repeat + query_index) % 2:
                modes.reverse()

            for mode in modes:
                start = time.perf_counter_ns()

                if mode == "global":
                    loop.run_until_complete(
                        store.similarity_search(
                            query_embedding.copy(),
                            k=args.k,
                        )
                    )
                else:
                    loop.run_until_complete(
                        store.similarity_search(
                            query_embedding.copy(),
                            k=args.k,
                            repository_id=target_repositories[query_index],
                        )
                    )

                elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
                latency_ms[mode].append(elapsed_ms)

    vector_bytes = size * args.dimension * np.dtype(np.float32).itemsize
    metadata_bytes = estimate_metadata_bytes(store.symbols)

    rows = []

    for mode in ("global", "scoped"):
        metric_names = quality_results[mode][0].keys()
        averaged_metrics = {
            name: statistics.mean(
                row[name] for row in quality_results[mode]
            )
            for name in metric_names
        }

        rows.append(
            {
                "index_size": size,
                "dimension": args.dimension,
                "mode": mode,
                "k": args.k,
                "p50_ms": percentile(latency_ms[mode], 50),
                "p95_ms": percentile(latency_ms[mode], 95),
                "recall_at_k": averaged_metrics[f"recall@{args.k}"],
                "precision_at_k": averaged_metrics[f"precision@{args.k}"],
                "mrr": averaged_metrics["mrr"],
                "ndcg_at_k": averaged_metrics[f"ndcg@{args.k}"],
                "faiss_vector_bytes_estimate": vector_bytes,
                "python_metadata_bytes_estimate": metadata_bytes,
                "faiss_candidates_per_query": (
                    min(args.k, size)
                    if mode == "global"
                    else scoped_candidate_count
                ),
            }
        )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[1000, 5000, 10000],
    )
    parser.add_argument("--dimension", type=int, default=64)
    parser.add_argument("--queries", type=int, default=10)
    parser.add_argument("--repositories", type=int, default=5)
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--relevant-per-query", type=int, default=10)
    parser.add_argument("--hard-negatives-per-query", type=int, default=12)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if (
        min(args.sizes) <= 0
        or args.dimension <= 0
        or args.queries <= 0
        or args.repositories < 2
        or args.k <= 0
        or args.repeats <= 0
        or args.warmups < 0
    ):
        parser.error("sizes, dimension, queries, k and repeats must be positive; repositories must be >= 2")

    original_index_path = SymbolVectorStore.INDEX_PATH
    original_metadata_path = SymbolVectorStore.METADATA_PATH

    loop = asyncio.new_event_loop()
    rows = []

    try:
        with tempfile.TemporaryDirectory(prefix="implementr-benchmark-") as directory:
            temp_dir = Path(directory)

            for size in args.sizes:
                print(f"Benchmarking index size {size}...", flush=True)
                rows.extend(benchmark_size(size, args, temp_dir, loop))
    finally:
        loop.close()
        SymbolVectorStore.INDEX_PATH = original_index_path
        SymbolVectorStore.METADATA_PATH = original_metadata_path

    columns = list(rows[0].keys())

    print()
    writer = csv.DictWriter(sys.stdout, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as file:
            output_writer = csv.DictWriter(file, fieldnames=columns)
            output_writer.writeheader()
            output_writer.writerows(rows)
        print(f"\nSaved benchmark results to {args.output}")


if __name__ == "__main__":
    main()
