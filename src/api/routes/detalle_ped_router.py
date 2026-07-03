from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.detalles_pedido import *
from src.db.session import get_db
from src.schemas.val_detalle_ped import detalles_pedido, detpedResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/detalle_pedido/register")
async def register_detalle_pedido(data: detalles_pedido, db: AsyncSession = Depends(get_db)):
    register = await registrar_detalle_ped(db, data.tallas, data.cantidad)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de pedido")

    return {"message": f"¡{register.tallas} Registrado con exito!", "status": "success"}

@router.get("/detalle_pedido", response_model=list[detpedResponse])
async def obtener_detalle_pedido(db: AsyncSession = Depends(get_db)):
    det_ped = await obt_detalle_ped(db)
    return det_ped

@router.delete("/detalle_pedido/{id}")
async def delete_detalle_pedido(id: int, db: AsyncSession = Depends(get_db)):
    detalle_ped = await del_detalle_ped(db, id)

    if not detalle_ped:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

    return {"Mensaje": "Detalle de pedido eliminado con exito"}

@router.put("/detalle_pedido/{id}")
async def update_detalle_pedido(id: int, new_tallas: int, new_cantidad: int, db: AsyncSession = Depends(get_db)):
    detalle_ped = await up_detalle_ped(db, id, new_tallas, new_cantidad)

    if not detalle_ped:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

    return {"Mensaje": "Detalle de pedido actualizado con exito"}