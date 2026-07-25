from fastapi import APIRouter, File, UploadFile, HTTPException, status

from app.api.health import router as health_router
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.schemas.upload import UploadResponse
from app.services.pdf_service import PDFService
from app.services.storage_service import StorageService

router = APIRouter()

router.include_router(health_router, prefix="/api")


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile | None = File(None)):
    if file is None or file.filename in (None, ""):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "missing_file",
                "message": "No file was uploaded.",
            },
        )

    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        if not (file.filename and file.filename.lower().endswith(".pdf")):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail={
                    "success": False,
                    "error_code": "unsupported_file_type",
                    "message": "Only PDF files are supported.",
                },
            )

    upload_service = StorageService()
    contents = await file.read()
    file_service = PDFService()

    try:
        summary = file_service.pdf_summary(contents, filename=file.filename)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "success": False,
                "error_code": "corrupt_pdf",
                "message": "The uploaded file is not a valid PDF.",
            },
        ) from exc

    uploaded_document = upload_service.save(file, subdirectory="uploads")
    document_summary = file_service.save_document(summary, uploaded_document)

    return UploadResponse(
        filename=document_summary.filename,
        page_count=document_summary.page_count,
        preview=summary.preview,
        character_count=summary.characters,
        storage_path=uploaded_document.storage_path,
        original_filename=uploaded_document.original_filename,
        stored_filename=uploaded_document.stored_filename,
        file_size=uploaded_document.file_size,
        mime_type=uploaded_document.mime_type,
    )


@router.get("/documents", response_model=DocumentListResponse)
async def get_documents():
    try:
        service = PDFService()
        documents = service.get_documents()
        return {"documents": documents}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "unexpected_error",
                "message": "An unexpected error occurred while retrieving documents.",
            },
        ) from exc


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int):
    try:
        service = PDFService()
        document = service.get_document(document_id)
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "document_not_found",
                    "message": "The requested document was not found.",
                },
            )
        return DocumentResponse.model_validate(document)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "unexpected_error",
                "message": "An unexpected error occurred while retrieving the document.",
            },
        ) from exc
