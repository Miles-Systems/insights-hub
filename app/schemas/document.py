from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    filename: str
    page_count: int
    uploaded_at: datetime

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]