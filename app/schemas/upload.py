from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str | None
    page_count: int
    preview: str | None
    character_count: int
    storage_path: str | None
    original_filename: str | None
    stored_filename: str | None
    file_size: int | None
    mime_type: str | None
