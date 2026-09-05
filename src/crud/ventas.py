from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.ganancias import ventas
from src.db.base import actividad
from sqlalchemy.future import select
from datetime import date, datetime

async def obt_ventas_mes(db: AsyncSession, year: int, month: int):
    query = select(ventas).where(
        ventas.is_active == True,
        extract('year', ventas.fecha) == year,
        extract('month', ventas.fecha) == month
    )
    result = await db.execute(query)
    return result.scalars().all()

async def registrar_venta(db: AsyncSession, fk_producto: int, precio_p: float, cantidad: int, fecha: date):
    new_venta = ventas(fk_producto=fk_producto, precio_p=precio_p, cantidad=cantidad, fecha=fecha)
    db.add(new_venta)
    await db.commit()
    await db.refresh(new_venta)
    return new_venta

async def obt_ventas(db: AsyncSession):
    query = select(ventas).where(ventas.is_active == True)
    result = await db.execute(query)
    ventas = result.scalars().all()
    return ventas

async def delventa(db: AsyncSession, id: int):
    act = await db.get(ventas, id)

    if not act:
        return act

    act.is_active = False
    await db.commit()
    await db.refresh(act)
    return act

async def up_venta(db: AsyncSession, id: int, new_fk_producto=int, new_precio_p=float, new_cantidad=int, new_fecha=date):
    act = await db.get(ventas, id)

    if not act:
        return None

    act.fk_producto = new_fk_producto
    act.precio_p = new_precio_p
    act.cantidad = new_cantidad
    act.fecha = new_fecha
    await db.commit()
    await db.refresh(act)
    return act