from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import pedido
from sqlalchemy.future import select

async def registrar_pedido(db: AsyncSession, fk_cliente: int, fk_producto: int):
    new_pedido = pedido(fk_cliente=fk_cliente, fk_producto=fk_producto)
    db.add(new_pedido)

    await db.commit()
    await db.refresh(new_pedido)
    return new_pedido

async def obt_pedido(db: AsyncSession):
    query = select(pedido).where(pedido.is_active == True)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def del_pedido(db: AsyncSession, id: int):
    pedido = await db.get(pedido, id)

    if not pedido:
        return pedido

    pedido.is_active = False
    await db.commit()
    await db.refresh(pedido)
    return pedido

async def up_pedido(db: AsyncSession, id: int, new_fk_cliente: int, new_fk_producto: int):
    pedido = await db.get(pedido, id)

    if not pedido:
        return None

    pedido.fk_cliente = new_fk_cliente
    pedido.fk_producto = new_fk_producto
    await db.commit()
    await db.refresh(pedido)
    return pedido