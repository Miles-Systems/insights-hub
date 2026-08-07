from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.exceptions import CorruptPdfError
from app.database.database import get_session
from app.models.document import Document, PDFSummary
from app.models.stored_file import StoredFile
from app.repositories.document_repository import DocumentRepository


class DocumentService:
    def pdf_summary(self, file_bytes: bytes, filename: str | None = None) -> PDFSummary:
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

        return PDFSummary(
            filename=filename,
            pages=pages,
            preview=preview,
            characters=len(full_text),
        )

    def save_document(
        self, summary: PDFSummary, uploaded_document: StoredFile
    ) -> Document:
        with get_session() as session:
            repository = DocumentRepository(session)
            document = Document(
                filename=summary.filename,
                page_count=summary.pages,
                character_count=summary.characters,
                storage_path=uploaded_document.storage_path,
                file_size=uploaded_document.file_size,
                mime_type=uploaded_document.mime_type,
            )
            repository.create(document)
            session.commit()
            session.refresh(document)
            return document

    def get_documents(self) -> list[Document]:
        with get_session() as session:
            repository = DocumentRepository(session)
            return repository.get_all()

    def get_document(self, document_id: int) -> Document | None:
        with get_session() as session:
            repository = DocumentRepository(session)
            document = repository.get_by_id(document_id)
            if document is None:
                return None
            return document
