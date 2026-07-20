from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.exceptions import CorruptPdfError
from app.database.database import get_session
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentResponse


class PDFService:
    def pdf_summary(self, file_bytes: bytes, filename: str | None = None) -> dict:
        try:
            reader = PdfReader(BytesIO(file_bytes))
        except PdfReadError as exc:
            raise CorruptPdfError() from exc

        pages = len(reader.pages)

        text_chunks = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_chunks.append(page_text)

        full_text = "\n".join(text_chunks)

        preview = full_text[:25].replace("\n", " ").strip()
        if len(full_text) > 25:
            preview += "..."

        return {
            "pages": pages,
            "characters": len(full_text),
            "preview": preview,
            "filename": filename,
        }

    def save_document(self, summary) -> Document:
        with get_session() as session:
            repository = DocumentRepository(session)
            document = Document(
                filename=summary["filename"],
                page_count=summary["pages"],
            )
            repository.create(document)
            session.commit()
            session.refresh(document)
            return document
        
    def get_documents(self) -> list[DocumentResponse]:
        with get_session() as session:
            repository = DocumentRepository(session)
            return repository.get_all()