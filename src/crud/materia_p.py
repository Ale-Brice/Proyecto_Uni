from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import materia_p
from sqlalchemy.future import select

async def registrar_materia_p(db: AsyncSession, tipo_material: str, precio_mat: float, cantidad: int):
    new_materia_p = materia_p(tipo_material=tipo_material, precio_mat=precio_mat, cantidad=cantidad)
    db.add(new_materia_p)
    await db.commit()
    await db.refresh(new_materia_p)
    return new_materia_p

async def obt_materia_p(db: AsyncSession):
    query = select(materia_p).where(materia_p.is_active == True)
    result = await db.execute(query)
    materiales = result.scalars().all()
    return materiales

async def del_materia_p(db: AsyncSession, id: int):
    mat = await db.get(materia_p, id)

    if not mat:
        return mat

    mat.is_active = False
    await db.commit()
    await db.refresh(mat)
    return mat

async def up_materia_p(db: AsyncSession, id: int, new_tipo_material: str, new_precio_mat: float, new_cantidad: int):
    mat = await db.get(materia_p, id)

    if not materia_p:
        return None

    mat.tipo_material = new_tipo_material
    mat.precio_mat = new_precio_mat
    mat.cantidad = new_cantidad
    await db.commit()
    await db.refresh(mat)
    return mat