from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import detalle_pro
from sqlalchemy.future import select

async def registrar_detalle_pro(db: AsyncSession, tallas: str, cantidad: int, fk_producto: int,):
    new_detalle_pro = detalle_pro(tallas=tallas, cantidad=cantidad, fk_producto = fk_producto)
    db.add(new_detalle_pro)
    await db.commit()
    await db.refresh(new_detalle_pro)
    return new_detalle_pro

async def obt_detalle_pro(db: AsyncSession):
    query = select(detalle_pro)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def del_detalle_pro(db: AsyncSession, id: int):
    det = await db.get(detalle_pro, id)

    if not det:
        return det

    det.is_active = False
    await db.commit()
    await db.refresh(det)
    return det

async def up_detalle_pro(db: AsyncSession, id: int, new_tallas: str, new_cantidad: int, new_fk_pro: int,):
    det = await db.get(detalle_pro, id)

    if not detalle_pro:
        return None

    det.tallas = new_tallas
    det.cantidad = new_cantidad
    det.fk_producto = new_fk_pro
    await db.commit()
    await db.refresh(det)
    return det