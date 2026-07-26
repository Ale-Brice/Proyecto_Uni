from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import cost_op
from sqlalchemy.future import select
from datetime import date

async def registrar_cost_op(db: AsyncSession, tipo_gasto_operativo: str, gasto_operativo: int, fecha: date):
    new_cost_op = cost_op(tipo_gasto_operativo = tipo_gasto_operativo, gasto_operativo = gasto_operativo, fecha = fecha)
    db.add(new_cost_op)
    await db.commit()
    await db.refresh(new_cost_op)
    return new_cost_op

async def obt_cost_op(db: AsyncSession):
    query = select(cost_op)
    result = await db.execute(query)
    costop = result.scalars().all()
    return costop

async def del_cost_op(db: AsyncSession, id: int):
    cost = await db.get(cost_op, id)

    if not cost:
        return cost

    cost.is_active = False
    await db.commit()
    await db.refresh(cost)
    return cost

async def up_cost_op(db: AsyncSession, id: int, new_tipo_gasto_operativo: str, new_gasto_operativo: int, new_fecha: date):
    cost = await db.get(cost_op, id)

    if not cost:
        return None

    cost.gasto_operativo = new_gasto_operativo
    cost.tipo_gasto_operativo = new_tipo_gasto_operativo
    cost.fecha = new_fecha
    await db.commit()
    await db.refresh(cost)
    return cost