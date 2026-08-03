from abc import ABC, abstractmethod

import numpy as np


class BaseEmbeddingModel(ABC):

    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """
        Dimension of vectors produced by this provider.
        """
        pass

    @abstractmethod
    async def embed_text(
        self,
        text: str,
    ) -> np.ndarray:
        pass

    @abstractmethod
    async def embed_texts(
        self,
        texts: list[str],
    ) -> np.ndarray:
        pass