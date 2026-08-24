from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.producto import *
from src.db.session import get_db
from src.schemas.val_producto import producto, proResponse
from sqlalchemy.future import select
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/producto/register")
async def register_producto(data: producto, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_producto(db, data.nombre_p, data.tipo_p, data.precio_p)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el producto")

    return {"message": f"¡{register.nombre_p} Registrado con exito!", "status": "success"}

@router.get("/producto", response_model=list[proResponse])
async def obtener_producto(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    pro = await obt_productos(db)
    return pro

@router.delete("/producto/{id}")
async def delete_producto(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    producto = await del_producto(db, id)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"Mensaje": "Producto eliminado con exito"}

@router.put("/producto/{id}")
async def update_producto(id: int, new_nombre_p: str, new_tipo_p: str, new_precio_p: float, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    producto = await up_producto(db, id, new_nombre_p, new_tipo_p, new_precio_p)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"Mensaje": "Producto actualizado con exito"}