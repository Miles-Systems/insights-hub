from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "unexpected_error",
            "message": "An unexpected error occurred.",
        },
    )


@app.get("/")
async def root():
    return {"message": "Insights Hub API"}
