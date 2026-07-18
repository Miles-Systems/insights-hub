from fastapi import APIRouter, File, UploadFile, HTTPException, status

from app.api.health import router as health_router
from app.database.database import get_session
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.upload import UploadResponse
from app.services import pdf_service

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

    try:
        result = pdf_service.pdf_summary(contents)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "success": False,
                "error_code": "corrupt_pdf",
                "message": "The uploaded file is not a valid PDF.",
            },
        ) from exc
    
    document = Document(
        filename=file.filename,
        page_count=result["pages"],
    )

    with get_session() as session:
        repo = DocumentRepository(session)
        repo.create(document)
        session.commit()
        session.refresh(document)

    return UploadResponse(
        filename=document.filename,
        page_count=document.page_count,
        preview=result["preview"],
        character_count=result["characters"],
    )