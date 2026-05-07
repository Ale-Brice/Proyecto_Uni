from fastapi import FastAPI, Depends, HTTPException
from src.db.session import get_db
from src.core.config import settings
from src.api.routes.usuarios_router import router as usuarios_router
from src.api.routes.registrar_router import router as registrar_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(usuarios_router, tags=["Usuarios"])
app.include_router(registrar_router, tags=["Usuarios"])