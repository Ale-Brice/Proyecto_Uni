from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.cost_op import *
from src.core.audit import get_audited_db
from src.schemas.val_cost_op import cost_op , costopResponse
from sqlalchemy.future import select


router = APIRouter()

@router.post("/cost_op/register")
async def register_cost_op(data: cost_op, db: AsyncSession = Depends(get_audited_db)):
    register = await registrar_cost_op(db, data.tipo_gasto_operativo, data.gasto_operativo, data.fecha)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el costo operativo")

    return {"message": f"¡Registrado con exito el gasto: {register.gasto_operativo}!", "status": "success"}

@router.get("/cost_op", response_model=list[costopResponse])
async def obtener_cost_op(db: AsyncSession = Depends(get_audited_db)):
    cost_op = await obt_cost_op(db)
    return cost_op

@router.delete("/cost_op/{id}")
async def delete_cost_op(id: int, db: AsyncSession = Depends(get_audited_db)):
    cost_op = await del_cost_op(db, id)

    if not cost_op:
        raise HTTPException(status_code=404, detail="Costo operativo no encontrado")

    return {"Mensaje": "Costo operativo eliminado con exito"}

@router.put("/cost_op/{id}")
async def update_cost_op(id: int, new_tipo_gasto_operativo : str, new_gasto_operativo : int , new_fecha : date, db: AsyncSession = Depends(get_audited_db)):
    cost_op = await up_cost_op(db, id, new_tipo_gasto_operativo, new_gasto_operativo, new_fecha)

    if not cost_op:
        raise HTTPException(status_code=404, detail="Costo operativo no encontrado")

    return {"Mensaje": "Costo operativo actualizado con exito"}