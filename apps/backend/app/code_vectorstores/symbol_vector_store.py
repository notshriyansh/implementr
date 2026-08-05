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

        self.embedding_dimension = (
            embedding_dimension
        )

        self.symbols: list[
            CodeSymbol
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
        symbols: list[
            CodeSymbol
        ],
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

        self.symbols.extend(
            symbols
        )

        self._persist()

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[
        CodeSymbol
    ]:

        query_embedding = (
            query_embedding.astype(
                "float32"
            )
        )

        faiss.normalize_L2(
            query_embedding
        )

        scores, indices = (
            self.index.search(
                query_embedding,
                k,
            )
        )

        scored_results = []

        for position, idx in enumerate(
            indices[0]
        ):

            if (
                idx == -1
                or idx >= len(
                    self.symbols
                )
            ):
                continue

            symbol = self.symbols[idx]

            score = (
                float(
                    scores[0][position]
                )
                * symbol.importance
            )

            scored_results.append(
                (
                    score,
                    symbol,
                )
            )

        scored_results.sort(
            reverse=True,
            key=lambda x: x[0],
        )

        return [
            symbol
            for _, symbol in scored_results
        ]