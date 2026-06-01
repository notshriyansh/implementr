from abc import ABC, abstractmethod

import numpy as np


class BaseEmbeddingModel(ABC):
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