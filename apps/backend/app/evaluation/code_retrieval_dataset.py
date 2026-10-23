from dataclasses import dataclass


@dataclass(frozen=True)
class CodeRetrievalBenchmarkCase:
    case_id: str
    question: str
    expected_files: tuple[str, ...]


CODE_RETRIEVAL_BENCHMARKS = (
    CodeRetrievalBenchmarkCase(
        case_id="chunking-001",
        question=(
            "How are source files split into fixed-size chunks, "
            "and how are their line ranges recorded?"
        ),
        expected_files=(
            "app/code_ingestion/code_chunker.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="scanning-001",
        question=(
            "How does repository scanning select supported source "
            "files and skip ignored directories?"
        ),
        expected_files=(
            "app/code_ingestion/repository_scanner.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="retrieval-001",
        question=(
            "How does code retrieval embed a query, request candidates, "
            "deduplicate files, and return the top results?"
        ),
        expected_files=(
            "app/code_retrieval/code_retrieval_service.py",
            "app/code_retrieval/retrieval_utils.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="deduplication-001",
        question=(
            "How are duplicate code chunks from the same repository "
            "file removed from retrieval results?"
        ),
        expected_files=(
            "app/code_retrieval/retrieval_utils.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="faiss-search-001",
        question=(
            "How does the code vector store normalize embeddings, "
            "perform FAISS similarity search, and filter by repository?"
        ),
        expected_files=(
            "app/code_vectorstores/code_vector_store.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="persistence-001",
        question=(
            "How are the code FAISS index and serialized chunk metadata "
            "saved and loaded?"
        ),
        expected_files=(
            "app/code_vectorstores/code_vector_store.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="chunk-embedding-001",
        question=(
            "What repository, file, language, and source-code information "
            "is included when embedding a code chunk?"
        ),
        expected_files=(
            "app/code_embeddings/code_embedding_model.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="symbol-embedding-001",
        question=(
            "How are code symbols converted into embedding text using "
            "their names, types, file paths, and implementation?"
        ),
        expected_files=(
            "app/code_embeddings/code_embedding_model.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="embedding-provider-001",
        question=(
            "How does dependency wiring select the configured embedding "
            "provider and construct the code embedding model?"
        ),
        expected_files=(
            "app/core/container.py",
        ),
    ),
    CodeRetrievalBenchmarkCase(
        case_id="sentence-transformer-001",
        question=(
            "How does the local SentenceTransformer implementation "
            "generate embeddings for individual texts and batches?"
        ),
        expected_files=(
            "app/embeddings/sentence_transformer.py",
        ),
    ),
)