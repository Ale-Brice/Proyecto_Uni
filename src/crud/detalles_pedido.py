from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import detalles_pedido
from sqlalchemy.future import select

async def registrar_detalle_ped(db: AsyncSession, fk_pedido: int, pe_desc: str, tallas: int, cantidad: int):
    new_detalle_ped = detalles_pedido(fk_pedido=fk_pedido, pe_desc=pe_desc, tallas=tallas, cantidad=cantidad)
    db.add(new_detalle_ped)
    await db.commit()
    await db.refresh(new_detalle_ped)
    return new_detalle_ped

async def obt_detalle_ped(db: AsyncSession):
    query = select(detalles_pedido).where(detalles_pedido.is_active == True)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def del_detalle_ped(db: AsyncSession, id: int):
    det = await db.get(detalles_pedido, id)

    if not det:
        return det

    det.is_active = False
    await db.commit()
    await db.refresh(det)
    return det

async def up_detalle_ped(db: AsyncSession, id: int, new_pe_desc: str, new_tallas: int, new_cantidad: int):
    det = await db.get(detalles_pedido, id)

    if not det:
        return None

    det.pe_desc = new_pe_desc
    det.tallas = new_tallas
    det.cantidad = new_cantidad
    await db.commit()
    await db.refresh(det)
    return det

async def update_detalle_pedP(db: AsyncSession, id: int, fk_pedido: int | None, pe_desc: str | None, tallas: int | None, cantidad: int | None):
    det = await db.get(detalles_pedido, id)
    if not det:
        return None
    if fk_pedido is not None:
        det.fk_pedido = fk_pedido
    if pe_desc is not None:
        det.pe_desc = pe_desc
    if tallas is not None:
        det.tallas = tallas
    if cantidad is not None:
        det.cantidad = cantidad
    await db.commit()
    await db.refresh(det)
    return det