from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.detalles_producto import *
from src.core.audit import get_audited_db
from src.schemas.val_detalle_pro import det_pro , detproResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/detalle_pro/register")
async def register_detalle_producto(data: det_pro, db: AsyncSession = Depends(get_audited_db)):
    register = await registrar_detalle_pro(db, data.tallas, data.cantidad, data.fk_producto)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de producto")

    return {"message": f"¡{register.tallas} Registrado con exito!", "status": "success"}

@router.get("/detalle_pro", response_model=list[detproResponse])
async def obtener_detalle_producto(db: AsyncSession = Depends(get_audited_db)):
    det_pro = await obt_detalle_pro(db)
    return det_pro

@router.delete("/detalle_pro/{id}")
async def delete_detalle_producto(id: int, db: AsyncSession = Depends(get_audited_db)):
    detalle_ped = await del_detalle_pro(db, id)

    if not detalle_ped:
        raise HTTPException(status_code=404, detail="Detalle de producto no encontrado")

    return {"Mensaje": "Detalle de producto eliminado con exito"}

@router.put("/detalle_pro/{id}")
async def update_detalle_producto(id: int, new_tallas: int, new_cantidad: int, new_fk_producto: int, db: AsyncSession = Depends(get_audited_db)):
    detalle_pro = await up_detalle_pro(db, id, new_tallas, new_cantidad, new_fk_producto)

    if not detalle_pro:
        raise HTTPException(status_code=404, detail="Detalle de producto no encontrado")

    return {"Mensaje": "Detalle de producto actualizado con exito"}