from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.actividades import *
from src.core.audit import get_audited_db
from src.schemas.val_actividades import actividad,actResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/actividad/register")
async def register_actividad(data: actividad, db: AsyncSession = Depends(get_audited_db)):
    register = await registrar_actividad(db, data.fk_empleado, data.fk_pedido, data.descripcion_tarea, data.fecha_inicio, data.fecha_final)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el empleado")

    return {"message": f"¡Actividad registrada con exito!", "status": "success"}

@router.get("/actividades", response_model=list[actResponse])
async def obtener_actividad(db: AsyncSession = Depends(get_audited_db)):
    act = await obt_actividad(db)
    return act

@router.delete("/actividades/{id}")
async def delete_actividad(id: int, db: AsyncSession = Depends(get_audited_db)):
    act = await delete_actividad(db, id)

    if not act:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    return {"Mensaje": "Actividad eliminada con exito"}

@router.put("/actividades/{id}")
async def update_actividad(id: int, fk_empleado: int, fk_pedido: int, descripcion_tarea: str, fecha_inicio: date, fecha_final: date, db: AsyncSession = Depends(get_audited_db)):
    act = await up_actividad(db, id, fk_empleado, fk_pedido, descripcion_tarea, fecha_inicio, fecha_final)

    if not act:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    return {"Mensaje": "Actividad actualizada con exito"}