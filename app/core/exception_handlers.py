from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import UploadError
from app.schemas.error import ErrorResponse

async def upload_error_handler(request: Request, exc: UploadError):
    payload = ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=payload.model_dump(),
    )


async def unexpected_error_handler(request: Request, exc: Exception):
    payload = ErrorResponse(
        error_code="unexpected_error",
        message="An unexpected error occurred.",
    )

    return JSONResponse(
        status_code=500,
        content=payload.model_dump(),
    )