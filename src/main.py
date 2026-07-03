from fastapi import FastAPI, Depends, HTTPException
from src.db.session import get_db
from src.core.config import settings
from src.api.routes.usuarios_router import router as usuarios_router
from src.api.routes.prueba_seguridad import router as prueba_seguridad_router
from src.api.routes.empleado_router import router as empleado_router
from src.api.routes.cliente_route import router as cliente_router
from src.api.routes.detalle_ped_router import router as detalle_ped_router
from src.api.routes.materia_p_router import router as materia_p_router
from src.api.routes.producto_router import router as producto_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(usuarios_router, tags=["Usuarios"])
app.include_router(empleado_router, tags=["Empleados"])
app.include_router(cliente_router, tags=["Clientes"])
app.include_router(detalle_ped_router, tags=["Detalles de Pedidos"])
app.include_router(materia_p_router, tags=["Materias Primas"])
app.include_router(producto_router, tags=["Productos"])
app.include_router(prueba_seguridad_router, tags=["Prueba de Seguridad"])