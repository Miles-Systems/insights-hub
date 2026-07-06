from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename: str | None
    page_count: int
    preview: str | None
    character_count: int