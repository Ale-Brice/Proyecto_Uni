from fastapi import FastAPI, Depends, HTTPException
from src.db.session import get_db
from src.core.config import settings
from src.api.routes.usuarios_router import router as usuarios_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])