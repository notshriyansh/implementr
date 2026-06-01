from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.document import ParsedDocument

class BaseParser(ABC):
    @abstractmethod
    async def parse(
        self,
        file_path: Path,
    ) -> ParsedDocument:
        pass