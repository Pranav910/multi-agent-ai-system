from fastapi import FastAPI
from .v1.endpoints import router as api_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")