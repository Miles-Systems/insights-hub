from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    page_count: int
    character_count: int | None
    storage_path: str | None  # TO DO: remove `none` when old records are removed
    file_size: int | None  # TO DO: remove `none` when old records are removed
    mime_type: str | None  # TO DO: remove `none` when old records are removed
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    documents: list[DocumentResponse]
