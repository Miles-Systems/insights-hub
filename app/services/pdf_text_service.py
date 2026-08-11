import fitz

from app.core.exceptions import PDFExtractionError
from app.models.extracted_page import ExtractedPage


class PDFTextService:
    def __init__(self, storage_service):
        self.storage_service = storage_service

    def extract_text(self, storage_path: str) -> list[ExtractedPage]:
        if not self.storage_service.exists(storage_path):
            raise FileNotFoundError(f"File not found at storage path: {storage_path}")

        path = self.storage_service.get_path(storage_path)
        extracted_pages: list[ExtractedPage] = []

        try:
            with fitz.open(path) as pdf:
                if len(pdf) == 0:
                    raise PDFExtractionError(
                        f"The PDF contains no pages at storage path: {storage_path}"
                    )

                for page in pdf:
                    text = page.get_text()
                    extracted_pages.append(
                        ExtractedPage(
                            page_number=page.number + 1,
                            text=text,
                        )
                    )

        except fitz.FileDataError as exc:
            raise PDFExtractionError(
                f"The file contains corrupted or unsupported PDF data "
                f"at storage path: {storage_path}"
            ) from exc

        return extracted_pages
