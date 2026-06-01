import json
import logging
from pathlib import Path

import faiss
import numpy as np

from app.schemas.chunk import DocumentChunk
from app.vectorstores.base import (
    BaseVectorStore,
)

logger = logging.getLogger(__name__)


class FAISSVectorStore(
    BaseVectorStore,
):
    INDEX_PATH = Path(
        "data/vector_store/faiss.index"
    )

    METADATA_PATH = Path(
        "data/vector_store/chunks.json"
    )

    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:
        self.embedding_dimension = (
            embedding_dimension
        )

        self.chunks: list[DocumentChunk] = []

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

        else:
            self.index = faiss.IndexFlatL2(
                self.embedding_dimension
            )

        if self.METADATA_PATH.exists():
            metadata = json.loads(
                self.METADATA_PATH.read_text()
            )

            self.chunks = [
                DocumentChunk(**chunk)
                for chunk in metadata
            ]

        logger.info(
            "Loaded %s chunks from disk",
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
        chunks: list[DocumentChunk],
    ) -> None:
        self.index.add(
            embeddings.astype("float32")
        )

        self.chunks.extend(chunks)

        self._persist()

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[DocumentChunk]:
        distances, indices = self.index.search(
            query_embedding.astype("float32"),
            k,
        )

        results: list[DocumentChunk] = []

        for index in indices[0]:
            if (
                index != -1
                and 0 <= index < len(self.chunks)
            ):
                results.append(
                    self.chunks[index]
                )

        return results