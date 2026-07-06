from fastapi import APIRouter, File, UploadFile
from app.api.health import router as health_router
from app.services import pdf_service

router = APIRouter()

router.include_router(health_router, prefix="/api")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    result = pdf_service.pdf_summary(contents)

    return {
        "filename": file.filename,
        "pages": result["pages"],
        "characters": result["characters"],
        "preview": result["preview"],
    }