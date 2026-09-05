from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.ventas import *
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker
from src.schemas.val_ventas import venta, ventaResponse
from sqlalchemy.future import select

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/venta/register")
async def register_venta(data: venta, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_venta(db, data.fk_producto, data.precio_p, data.cantidad, data.fecha)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el producto")

    return {"message": f"¡Venta registrada con exito!", "status": "success"}

@router.get("/ventas", response_model=list[ventaResponse])
async def obtener_ventas(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    ventas = await obt_ventas(db)
    return ventas

@router.delete("/ventas/{id}")
async def delete_venta(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    act = await delventa(db, id)

    if not act:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    return {"Mensaje": "Venta eliminada con exito"}

@router.put("/ventas/{id}")
async def update_venta(id: int, fk_producto: int, precio_p: float, cantidad: int, fecha: date, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    act = await up_venta(db, id, fk_producto, precio_p, cantidad, fecha)

    if not act:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    return {"Mensaje": "Venta actualizada con exito"}