from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.pedidos import *
from src.core.audit import get_audited_db
from src.schemas.val_pedido import pedido, pedResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/pedido/register")
async def register_pedido(data: pedido, db: AsyncSession = Depends(get_audited_db)):
    register = await registrar_pedido(db, fk_cliente=data.fk_cliente, fk_producto=data.fk_producto)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de pedido")

    return {"message": f"¡Registrado con exito!", "status": "success"}

@router.get("/pedido", response_model=list[pedResponse])
async def obtener_pedido(db: AsyncSession = Depends(get_audited_db)):
    ped = await obt_pedido(db)
    return ped

@router.delete("/pedido/{id}")
async def delete_pedido(id: int, db: AsyncSession = Depends(get_audited_db)):
    pedido = await del_pedido(db, id)

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return {"Mensaje": "Pedido eliminado con exito"}

@router.put("/pedido/{id}")
async def update_pedido(id: int, new_fk_cliente: int, new_fk_producto: int, db: AsyncSession = Depends(get_audited_db)):
    ped = await up_pedido(db, id, new_fk_cliente, new_fk_producto)

    if not ped:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return {"Mensaje": "Pedido actualizado con exito"}