from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.document_content import DocumentContent


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    page_count: Mapped[int] = mapped_column(default=0)
    character_count: Mapped[int] = mapped_column(default=0, nullable=True)
    storage_path: Mapped[str] = mapped_column(String(255), nullable=True)
    file_size: Mapped[int] = mapped_column(default=0, nullable=True)
    mime_type: Mapped[str] = mapped_column(String(50), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    contents: Mapped[list["DocumentContent"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, filename='{self.filename}')>"


@dataclass
class PDFSummary:
    filename: str
    pages: int
    preview: str
    characters: int
