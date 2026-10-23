from app.code_embeddings.code_embedding_model import CodeEmbeddingModel
from app.code_ingestion.code_chunker import CodeChunker
from app.code_ingestion.repository_scanner import RepositoryScanner
from app.code_retrieval.code_retrieval_service import CodeRetrievalService
from app.code_vectorstores.code_vector_store import CodeVectorStore
from app.core.config import get_settings
from app.core.container import Container
from app.evaluation.code_retrieval_benchmark import (
    evaluate_code_retrieval,
    summarize_code_retrieval_results,
)
from app.evaluation.code_retrieval_dataset import CODE_RETRIEVAL_BENCHMARKS

import argparse
import asyncio
import csv
import hashlib
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import faiss

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


logger = logging.getLogger("code_retrieval_benchmark")


def collect_repository_chunks(
    root: Path,
) -> tuple[str, list, int]:
    root = root.resolve()
    repository_id = hashlib.sha256(
        str(root).encode("utf-8")
    ).hexdigest()[:16]

    scanner = RepositoryScanner()
    chunker = CodeChunker()

    files = scanner.scan(str(root))
    scanned_paths = {
        path.relative_to(root).as_posix()
        for path in files
    }

    expected_paths = {
        path
        for case in CODE_RETRIEVAL_BENCHMARKS
        for path in case.expected_files
    }

    missing_paths = expected_paths - scanned_paths
    if missing_paths:
        raise ValueError(
            "Benchmark labels reference files that were not scanned: "
            f"{sorted(missing_paths)}"
        )

    chunks = []
    for path in files:
        chunks.extend(
            chunker.chunk_file(
                file_path=path,
                repository_root=root,
                repository_name=root.name,
                repository_id=repository_id,
            )
        )

    if not chunks:
        raise ValueError(f"No code chunks found under {root}")

    chunked_paths = {chunk.relative_path.replace("\\", "/") for chunk in chunks}
    empty_labeled_files = expected_paths - chunked_paths
    if empty_labeled_files:
        raise ValueError(
            f"{sorted(empty_labeled_files)}"
        )

    return repository_id, chunks, len(files)


def write_csv(path: Path, results: list[dict], k: int) -> None:
    fields = [
        "case_id",
        "question",
        "expected_files",
        "retrieved_files",
        "latency_ms",
        f"recall@{k}",
        f"precision@{k}",
        "reciprocal_rank",
        f"ndcg@{k}",
    ]

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()

        for result in results:
            row = dict(result)
            row["expected_files"] = ";".join(result["expected_files"])
            row["retrieved_files"] = ";".join(result["retrieved_files"])
            writer.writerow(row)



async def run_benchmark(
    k: int,
    provider: str = "local",
    batch_size: int = 16,
) -> None:
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    root = BACKEND_ROOT.resolve()
    repository_id, chunks, scanned_file_count = collect_repository_chunks(root)

    settings = get_settings()

    if provider == "local":
        from app.embeddings.sentence_transformer import (
            SentenceTransformerEmbeddingModel,
        )

        embedding_model = SentenceTransformerEmbeddingModel()
        embedding_provider = "local"
        model_name = "all-MiniLM-L6-v2"
    elif provider == "configured":
        container = Container()
        embedding_model = container.embedding_model
        embedding_provider = settings.embedding_provider
        model_name = (
            settings.jina_embedding_model
            if embedding_provider == "jina"
            else "all-MiniLM-L6-v2"
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    code_embedding_model = CodeEmbeddingModel(embedding_model)
    dimension = embedding_model.embedding_dimension

    output_dir = root / "benchmark-results"
    output_dir.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory(
        prefix="implementr-code-retrieval-"
    ) as temp_dir:
        temp_path = Path(temp_dir)

        vector_store = CodeVectorStore.__new__(CodeVectorStore)
        vector_store.embedding_dimension = dimension
        vector_store.chunks = []
        vector_store.index = faiss.IndexFlatIP(dimension)
        vector_store.INDEX_PATH = temp_path / "code.index"
        vector_store.METADATA_PATH = temp_path / "chunks.json"

        retrieval_service = CodeRetrievalService(
            embedding_model=code_embedding_model,
            vector_store=vector_store,
        )

        logger.info(
            "Indexing %s chunks from %s source files using %s "
            "in batches of %s",
            len(chunks),
            scanned_file_count,
            embedding_provider,
            batch_size,
        )

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]

            embeddings = await code_embedding_model.embed_chunks(batch)

            await vector_store.add_embeddings(
                embeddings=embeddings,
                chunks=batch,
            )

            indexed = start + len(batch)
            logger.info(
                "Indexed %s/%s chunks",
                indexed,
                len(chunks),
            )

        results = await evaluate_code_retrieval(
            retrieval_service=retrieval_service,
            cases=CODE_RETRIEVAL_BENCHMARKS,
            repository_id=repository_id,
            k=k,
        )

        summary = summarize_code_retrieval_results(results, k=k)

    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": root.name,
        "embedding_provider": embedding_provider,
        "embedding_model": model_name,
        "embedding_dimension": dimension,
        "index_batch_size": batch_size,
        "scanned_source_files": scanned_file_count,
        "indexed_chunks": len(chunks),
        "benchmark_cases": len(CODE_RETRIEVAL_BENCHMARKS),
        "metrics": summary,
    }

    csv_path = output_dir / "code-retrieval-baseline.csv"
    json_path = output_dir / "code-retrieval-baseline-summary.json"

    write_csv(csv_path, results, k)
    json_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print("\nCode retrieval baseline")
    print("-----------------------")
    print(f"Embedding provider: {embedding_provider}")
    print(f"Embedding model:    {model_name}")
    print(f"Index batch size:   {batch_size}")
    print(f"Source files:       {scanned_file_count}")
    print(f"Indexed chunks:     {len(chunks)}")
    print(f"Benchmark cases:    {len(results)}")

    for name, value in summary.items():
        if name not in {"case_count", "k"}:
            print(f"{name:22s} {value:.4f}")

    print(f"\nDetailed results: {csv_path}")
    print(f"Summary:          {json_path}")



def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate Implementr code retrieval on labeled backend questions."
        )
    )
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Number of distinct files to retrieve per question.",
    )
    parser.add_argument(
        "--provider",
        choices=("local", "configured"),
        default="local",
        help="Embedding provider; defaults to local to avoid API usage.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Number of code chunks to embed per indexing batch.",
    )
    args = parser.parse_args()

    if args.k < 1:
        parser.error("--k must be at least 1")
    if args.batch_size < 1:
        parser.error("--batch-size must be at least 1")

    logging.basicConfig(level=logging.INFO)
    asyncio.run(
        run_benchmark(
            k=args.k,
            provider=args.provider,
            batch_size=args.batch_size,
        )
    )


if __name__ == "__main__":
    main()
