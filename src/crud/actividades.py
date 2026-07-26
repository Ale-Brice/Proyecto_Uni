from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import actividad
from sqlalchemy.future import select
from datetime import datetime

async def registrar_actividad(db: AsyncSession, fk_empleado: int, fk_pedido: int, descripcion_tarea: str, fecha_incio: datetime, fecha_final: datetime):
    new_actividad = actividad(fk_empleado=fk_empleado, fk_pedido=fk_pedido, descripcion_tarea=descripcion_tarea, fecha_incio=fecha_incio, fecha_final=fecha_final)
    db.add(new_actividad)
    await db.commit()
    await db.refresh(new_actividad)
    return new_actividad

async def obt_actividad(db: AsyncSession):
    query = select(actividad).where(actividad.is_active == True)
    result = await db.execute(query)
    actividades = result.scalars().all()
    return actividades

async def delactividad(db: AsyncSession, id: int):
    act = await db.get(actividad, id)

    if not act:
        return act

    act.is_active = False
    await db.commit()
    await db.refresh(act)
    return act

async def up_actividad(db: AsyncSession, id: int, new_fk_empleado=int, new_fk_pedido=int, new_descripcion_tarea=str, new_fecha_incio=datetime, new_fecha_final=datetime):
    act = await db.get(actividad, id)

    if not act:
        return None

    act.fk_empleado = new_fk_empleado
    act.fk_pedido = new_fk_pedido
    act.descripcion_tarea = new_descripcion_tarea
    act.fecha_inicio = new_fecha_incio
    act.fecha_final = new_fecha_final
    await db.commit()
    await db.refresh(act)
    return act