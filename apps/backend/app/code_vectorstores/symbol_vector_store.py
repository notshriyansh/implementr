import json
import logging
from pathlib import Path

import faiss
import numpy as np

from app.schemas.code_symbol import (
    CodeSymbol,
)

logger = logging.getLogger(__name__)


class SymbolVectorStore:

    INDEX_PATH = Path(
        "data/symbol_vector_store/symbol.index"
    )

    METADATA_PATH = Path(
        "data/symbol_vector_store/symbols.json"
    )

    def __init__(
        self,
        embedding_dimension: int,
    ) -> None:

        self.embedding_dimension = embedding_dimension

        self.symbols: list[CodeSymbol] = []

        self._repository_indexes: dict[str, faiss.Index] = {}
        self._repository_symbol_indices: dict[str, list[int]] = {}

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
                "Loaded Symbol FAISS dimension: %s",
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

            self.symbols = [
                CodeSymbol(**symbol)
                for symbol in metadata
            ]

        logger.info(
            "Loaded %s symbols",
            len(self.symbols),
        )

        self._rebuild_repository_indexes()

    def _rebuild_repository_indexes(self) -> None:
        self._repository_indexes = {}
        self._repository_symbol_indices = {}

        if not self.symbols:
            return

        if self.index.ntotal != len(self.symbols):
            raise ValueError(
                "Symbol FAISS index and metadata are inconsistent: "
                f"{self.index.ntotal} vectors but {len(self.symbols)} symbols."
            )

        vectors_by_repository: dict[str, list[np.ndarray]] = {}

        for global_index, symbol in enumerate(self.symbols):
            vector = self.index.reconstruct(global_index)
            vectors_by_repository.setdefault(
                symbol.repository_id, []
            ).append(vector)

            self._repository_symbol_indices.setdefault(
                symbol.repository_id, []
            ).append(global_index)

        for repository_id, vectors in vectors_by_repository.items():
            repository_index = faiss.IndexFlatIP(
                self.embedding_dimension
            )
            repository_index.add(
                np.asarray(vectors, dtype=np.float32)
            )
            self._repository_indexes[repository_id] = repository_index

    def _persist(
        self,
    ) -> None:

        faiss.write_index(
            self.index,
            str(self.INDEX_PATH),
        )

        metadata = [
            symbol.model_dump()
            for symbol in self.symbols
        ]

        self.METADATA_PATH.write_text(
            json.dumps(
                metadata,
                indent=2,
            )
        )

    async def add_symbols(
        self,
        embeddings: np.ndarray,
        symbols: list[CodeSymbol],
    ) -> None:
        if len(embeddings) != len(symbols):
            raise ValueError(
                "The number of embeddings must match the number of symbols."
            )

        if not symbols:
            return

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        ).copy()

        if embeddings.ndim != 2 or embeddings.shape[1] != self.embedding_dimension:
            raise ValueError(
                f"Expected embeddings with shape (n, {self.embedding_dimension})."
            )

        faiss.normalize_L2(embeddings)

        global_start = len(self.symbols)

        self.index.add(embeddings)
        self.symbols.extend(symbols)

        for offset, symbol in enumerate(symbols):
            repository_id = symbol.repository_id
            vector = embeddings[offset : offset + 1]

            if repository_id not in self._repository_indexes:
                self._repository_indexes[repository_id] = faiss.IndexFlatIP(
                    self.embedding_dimension
                )
                self._repository_symbol_indices[repository_id] = []

            self._repository_indexes[repository_id].add(vector)
            self._repository_symbol_indices[repository_id].append(
                global_start + offset
            )

        self._persist()

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        repository_id: str | None = None,
    ) -> list[CodeSymbol]:
        if k <= 0 or self.index.ntotal == 0:
            return []

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32,
        ).copy()

        if (
            query_embedding.ndim != 2
            or query_embedding.shape[0] != 1
            or query_embedding.shape[1] != self.embedding_dimension
        ):
            raise ValueError(
                "Expected query embedding with shape "
                f"(1, {self.embedding_dimension})."
            )

        faiss.normalize_L2(query_embedding)

        if repository_id is None:
            search_index = self.index
            global_indices = None
        else:
            search_index = self._repository_indexes.get(repository_id)

            if search_index is None or search_index.ntotal == 0:
                return []

            global_indices = self._repository_symbol_indices[repository_id]

        search_k = (
            search_index.ntotal
            if repository_id is not None
            else min(k, search_index.ntotal)
        )

        scores, indices = search_index.search(
            query_embedding,
            search_k,
        )

        ranked_symbols: list[tuple[float, CodeSymbol]] = []

        for position, local_index in enumerate(indices[0]):
            if local_index < 0:
                continue

            symbol_index = (
                int(local_index)
                if global_indices is None
                else global_indices[int(local_index)]
            )

            if symbol_index >= len(self.symbols):
                continue

            symbol = self.symbols[symbol_index]
            score = float(scores[0][position]) * symbol.importance
            ranked_symbols.append((score, symbol))

        ranked_symbols.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            symbol
            for _, symbol in ranked_symbols[:k]
        ]