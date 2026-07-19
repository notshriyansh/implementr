from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseLLM(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
    ) -> str:
        pass

    @abstractmethod
    def stream_generate(
        self,
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        pass