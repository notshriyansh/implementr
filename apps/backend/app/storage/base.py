from abc import ABC, abstractmethod
from pathlib import Path

class BaseStorage(ABC):
    @abstractmethod
    async def save_file(
        self,
        content: bytes,
        user_id: str,
        filename: str,
    )-> Path:
        pass

    @abstractmethod
    async def file_exists(
        self,
        user_id: str,
        filename: str,
    ) -> bool:
        pass