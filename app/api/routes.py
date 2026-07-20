from fastapi import APIRouter, File, UploadFile, HTTPException, status

from app.api.health import router as health_router
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.schemas.upload import UploadResponse
from app.services.pdf_service import PDFService

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

    contents = await file.read()
    service = PDFService()

    try:
        summary = service.pdf_summary(contents, filename=file.filename)
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

    document = service.save_document(summary)

    return UploadResponse(
        filename=document.filename,
        page_count=document.page_count,
        preview=summary["preview"],
        character_count=summary["characters"],
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
