import json
import logging
from pathlib import Path

import faiss
import numpy as np

from app.schemas.code_chunk import CodeChunk

logger = logging.getLogger(__name__)


class CodeVectorStore:
    INDEX_PATH = Path(
        "data/code_vector_store/code.index"
    )

    METADATA_PATH = Path(
        "data/code_vector_store/chunks.json"
    )

    def __init__(
        self,
        embedding_dimension: int,
    ) -> None:

        self.embedding_dimension = (
            embedding_dimension
        )

        self.chunks: list[
            CodeChunk
        ] = []

        self._load_or_create_index()

    def _load_or_create_index(
        self,
    ) -> None:

        self.INDEX_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.INDEX_PATH.exists():

            self.index = faiss.read_index(
                str(self.INDEX_PATH)
            )

            logger.info(
                "Loaded Code FAISS dimension: %s",
                self.index.d,
            )

        else:

            self.index = faiss.IndexFlatIP(
                self.embedding_dimension
            )

        if self.METADATA_PATH.exists():

            metadata = json.loads(
                self.METADATA_PATH.read_text()
            )

            self.chunks = [
                CodeChunk(**chunk)
                for chunk in metadata
            ]

        logger.info(
            "Loaded %s code chunks",
            len(self.chunks),
        )

    def _persist(
        self,
    ) -> None:

        faiss.write_index(
            self.index,
            str(self.INDEX_PATH),
        )

        metadata = [
            chunk.model_dump()
            for chunk in self.chunks
        ]

        self.METADATA_PATH.write_text(
            json.dumps(
                metadata,
                indent=2,
            )
        )

    async def add_embeddings(
        self,
        embeddings: np.ndarray,
        chunks: list[CodeChunk],
    ) -> None:

        embeddings = embeddings.astype(
            "float32"
        )

        faiss.normalize_L2(
            embeddings
        )

        self.index.add(
            embeddings
        )

        self.chunks.extend(
            chunks
        )

        self._persist()


    async def replace_repository(
        self,
        repository_id: str,
        embeddings: np.ndarray,
        chunks: list[CodeChunk],
    ) -> None:
        if len(embeddings) != len(chunks):
            raise ValueError(
                "The number of embeddings must match the number of chunks."
            )

        if any(
            chunk.repository_id != repository_id
            for chunk in chunks
        ):
            raise ValueError(
                "All replacement chunks must belong to the specified repository."
            )

        new_embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        ).copy()

        if (
            new_embeddings.ndim != 2
            or new_embeddings.shape[1] != self.embedding_dimension
        ):
            raise ValueError(
                f"Expected embeddings with shape (n, {self.embedding_dimension})."
            )

        if not np.isfinite(new_embeddings).all():
            raise ValueError("Embeddings must contain only finite values.")

        faiss.normalize_L2(new_embeddings)

        if self.index.ntotal != len(self.chunks):
            raise ValueError(
                "Code FAISS index and metadata are inconsistent: "
                f"{self.index.ntotal} vectors but {len(self.chunks)} chunks."
            )

        preserved_vectors = []
        preserved_chunks = []

        for index, chunk in enumerate(self.chunks):
            if chunk.repository_id == repository_id:
                continue

            preserved_vectors.append(
                self.index.reconstruct(index)
            )
            preserved_chunks.append(chunk)

        replacement_index = faiss.IndexFlatIP(
            self.embedding_dimension
        )

        if preserved_vectors:
            replacement_index.add(
                np.asarray(
                    preserved_vectors,
                    dtype=np.float32,
                )
            )

        if len(new_embeddings):
            replacement_index.add(new_embeddings)

        replacement_chunks = (
            preserved_chunks + chunks
        )

        self.index = replacement_index
        self.chunks = replacement_chunks

        self._persist()


    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        repository_id: str | None = None,
    ) -> list[CodeChunk]:
        if k <= 0 or self.index.ntotal == 0:
            return []

        query_embedding = query_embedding.astype("float32")
        faiss.normalize_L2(query_embedding)

        search_k = (
            self.index.ntotal
            if repository_id is not None
            else k
        )

        _, indices = self.index.search(query_embedding, search_k)

        results: list[CodeChunk] = []

        for idx in indices[0]:
            if idx == -1 or idx >= len(self.chunks):
                continue

            chunk = self.chunks[idx]

            if (
                repository_id is not None
                and chunk.repository_id != repository_id
            ):
                continue

            results.append(chunk)

            if repository_id is None and len(results) == k:
                break

        return results
