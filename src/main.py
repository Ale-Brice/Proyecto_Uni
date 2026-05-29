from fastapi import FastAPI, Depends, HTTPException
from src.db.session import get_db
from src.core.config import settings
from src.api.routes.usuarios_router import router as usuarios_router
from src.api.routes.obtener_usuario import router as obtener_usuario
from src.api.routes.delete_usuarios import router as eliminar_usuario
from src.api.routes.prueba_seguridad import router as prueba_seguridad_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(usuarios_router, tags=["Usuarios"])
app.include_router(obtener_usuario, tags=["Usuarios"])
app.include_router(prueba_seguridad_router, tags=["Prueba de Seguridad"])
app.include_router(eliminar_usuario, tags=["Usuarios"])