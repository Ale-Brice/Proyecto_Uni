from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import producto
from sqlalchemy.future import select

async def registrar_producto(db: AsyncSession, nombre_p: str, tipo_p: str, precio_p: float):
    new_producto = producto(nombre_p=nombre_p, tipo_p=tipo_p, precio_p=precio_p)
    db.add(new_producto)
    await db.commit()
    await db.refresh(new_producto)
    return new_producto

async def obt_productos(db: AsyncSession):
    query = select(producto).where(producto.is_active == True)
    result = await db.execute(query)
    productos = result.scalars().all()
    return productos

async def del_producto(db: AsyncSession, id: int):
    pro = await db.get(producto, id)

    if not pro:
        return pro

    pro.is_active = False
    await db.commit()
    await db.refresh(pro)
    return pro

async def up_producto(db: AsyncSession, id: int, new_nombre_p: str, new_tipo_p: str, new_precio_p: float):
    pro = await db.get(producto, id)

    if not producto:
        return None

    pro.nombre_p = new_nombre_p
    pro.tipo_p = new_tipo_p
    pro.precio_p = new_precio_p
    await db.commit()
    await db.refresh(pro)
    return pro

async def update_productoP(db: AsyncSession, id: int, nombre_p: str, tipo_p: str, precio_p: float):
    prod = await db.get(producto, id)
    if not prod:
        return None
    if nombre_p is not None:
        prod.nombre_p = nombre_p
    if tipo_p is not None:
        prod.tipo_p = tipo_p
    if precio_p is not None:
        prod.precio_p = precio_p
    await db.commit()
    await db.refresh(prod)
    return prod