from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import cost_adm
from sqlalchemy.future import select
from datetime import date

async def registrar_cost_adm(db: AsyncSession, tipo_costo: str, gasto_administrativo: int, fecha: date):
    new_cost_adm = cost_adm(tipo_costo = tipo_costo, gasto_administrativo = gasto_administrativo, fecha = fecha)
    db.add(new_cost_adm)
    await db.commit()
    await db.refresh(new_cost_adm)
    return new_cost_adm

async def obt_cost_adm(db: AsyncSession):
    query = select(cost_adm)
    result = await db.execute(query)
    costadms = result.scalars().all()
    return costadms

async def del_cost_adm(db: AsyncSession, id: int):
    cost = await db.get(cost_adm, id)

    if not cost:
        return cost

    cost.is_active = False
    await db.commit()
    await db.refresh(cost)
    return cost

async def up_cost_adm(db: AsyncSession, id: int, new_tipo_costo: str, new_gasto_administrativo: int, new_fecha: date):
    cost = await db.get(cost_adm, id)

    if not cost:
        return None

    cost.gasto_administrativo = new_gasto_administrativo
    cost.tipo_costo = new_tipo_costo
    cost.fecha = new_fecha
    await db.commit()
    await db.refresh(cost)
    return cost