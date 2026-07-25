from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.models.stored_file import StoredFile

BASE_STORAGE_PATH = Path("storage")


class StorageService:
    def save(self, file: UploadFile, subdirectory: str) -> StoredFile:
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid4()}{file_extension}"

        relative_target_dir = Path(subdirectory)
        relative_stored_path = relative_target_dir / unique_filename

        full_path = BASE_STORAGE_PATH / relative_stored_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        file.file.seek(0)
        file_content = file.file.read()
        actual_file_size = len(file_content)

        with open(full_path, "wb") as f:
            f.write(file_content)

        return StoredFile(
            storage_path=str(relative_stored_path.as_posix()),
            original_filename=file.filename,
            stored_filename=unique_filename,
            file_size=actual_file_size,
            mime_type=file.content_type,
        )

    # def read(self, storage_path: str) -> bytes: ...
    # def delete(self, storage_path: str) -> None: ...
    # def exists(self, storage_path: str) -> bool: ...
