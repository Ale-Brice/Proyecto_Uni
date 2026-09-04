from sqlalchemy import extract
from sqlalchemy.future import select
from src.db.base import *
from sqlalchemy.ext.asyncio import AsyncSession

async def obt_cost_adm_mes(db: AsyncSession, year: int, month: int):
    query = select(cost_adm).where(
        extract('year', cost_adm.fecha) == year,
        extract('month', cost_adm.fecha) == month
    )
    result = await db.execute(query)
    return result.scalars().all()

async def obt_cost_op_mes(db: AsyncSession, year: int, month: int):
    query = select(cost_op).where(
        extract('year', cost_op.fecha) == year,
        extract('month', cost_op.fecha) == month
    )
    result = await db.execute(query)
    return result.scalars().all()

async def obt_materia_p_mes(db: AsyncSession, year: int, month: int):
    query = select(materia_p).where(
        materia_p.is_active == True,
        extract('year', materia_p.fecha) == year,
        extract('month', materia_p.fecha) == month
    )
    result = await db.execute(query)
    return result.scalars().all()