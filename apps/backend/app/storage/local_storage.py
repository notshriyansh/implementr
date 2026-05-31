from pathlib import Path

from app.storage.base import BaseStorage

class LocalStorage(BaseStorage):
    BASE_PATH = Path("data/papers")

    async def save_file(
            self,
            content: bytes,
            user_id: str,
            filename: str,
    ) -> Path:
        user_dir = self.BASE_PATH / user_id

        user_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = user_dir / filename

        file_path.write_bytes(content)

        return file_path
    
    async def file_exists(
            self,
            user_id: str,
            filename: str,
    ) -> bool:
        file_path = (
            self.BASE_PATH
            / user_id
            / filename
        )

        return file_path.exists()