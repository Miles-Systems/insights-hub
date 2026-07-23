from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    page_count: int
    character_count: int | None
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    documents: list[DocumentResponse]
