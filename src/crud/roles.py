from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.db.base import rol, permiso, permiso_rol, rol_usuario
from sqlalchemy.future import select

async def registrar_rol(db: AsyncSession, nombre_rol: str):
    new_rol = rol(nombre_rol=nombre_rol)
    db.add(new_rol)

    await db.commit()
    await db.refresh(new_rol)
    return new_rol

async def obt_rol(db: AsyncSession):
    query = select(rol).where(rol.is_active == True)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def obt_rol_eliminado(db: AsyncSession):
    query = select(rol).where(rol.is_active == False)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def registrar_permiso(db: AsyncSession, nombre_permiso: str):
    new_permiso = permiso(nombre_permiso=nombre_permiso)
    db.add(new_permiso)

    await db.commit()
    await db.refresh(new_permiso)
    return new_permiso

async def obt_permiso(db: AsyncSession):
    query = select(permiso).where(permiso.is_active == True)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def obt_permiso_eliminado(db: AsyncSession):
    query = select(permiso).where(permiso.is_active == False)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def registrar_permiso_rol(db: AsyncSession, fk_id_rol: int, fk_id_permiso: int):
    new_permiso_rol = permiso_rol(fk_id_rol=fk_id_rol, fk_id_permiso=fk_id_permiso)
    db.add(new_permiso_rol)

    await db.commit()
    await db.refresh(new_permiso_rol)
    return new_permiso_rol

async def obt_permiso_rol(db: AsyncSession):
    query = select(permiso_rol).where(permiso_rol.is_active == True)
    result = await db.execute(query)
    detalles = result.scalars().all()
    return detalles

async def del_permiso_rol(db: AsyncSession, id: int):
    stmt = select(permiso_rol).where(permiso_rol.id_permiso_rol == id)
    result = await db.execute(stmt)
    per_rol = result.scalar_one_or_none()
    if per_rol:
        await db.delete(per_rol)
        await db.commit()

    return per_rol

async def del_rol(db: AsyncSession, id: int):
    stmt = select(rol).where(rol.id_rol == id)
    result = await db.execute(stmt)
    rol_db = result.scalar_one_or_none()
    if rol_db:
        if rol_db.nombre_rol.lower() == "admin":
            return "admin"
        rol_db.is_active = False
        await db.commit()
        await db.refresh(rol_db)
    return rol_db


async def restaurar_rol(db: AsyncSession, id: int):
    stmt = select(rol).where(rol.id_rol == id)
    result = await db.execute(stmt)
    rol_db = result.scalar_one_or_none()
    if rol_db:
        rol_db.is_active = True
        await db.commit()
        await db.refresh(rol_db)
    return rol_db


async def del_permiso(db: AsyncSession, id: int):
    stmt = select(permiso).where(permiso.id_permiso == id)
    result = await db.execute(stmt)
    permiso_db = result.scalar_one_or_none()
    if permiso_db:
        permiso_db.is_active = False
        await db.commit()
        await db.refresh(permiso_db)
    return permiso_db


async def restaurar_permiso(db: AsyncSession, id: int):
    stmt = select(permiso).where(permiso.id_permiso == id)
    result = await db.execute(stmt)
    permiso_db = result.scalar_one_or_none()
    if permiso_db:
        permiso_db.is_active = True
        await db.commit()
        await db.refresh(permiso_db)
    return permiso_db

async def registrar_rol_usuario(db: AsyncSession, fk_id_usuario: int, fk_id_rol: int):
    new_rol_usuario = rol_usuario(fk_id_usuario=fk_id_usuario, fk_id_rol=fk_id_rol)
    db.add(new_rol_usuario)
    await db.commit()
    await db.refresh(new_rol_usuario)
    return new_rol_usuario


async def obt_rol_usuario(db: AsyncSession):
    query = select(rol_usuario).where(rol_usuario.is_active == True)
    result = await db.execute(query)
    return result.scalars().all()


async def del_rol_usuario(db: AsyncSession, id: int):
    stmt = select(rol_usuario).where(rol_usuario.id_rol_user == id)
    result = await db.execute(stmt)
    rel = result.scalar_one_or_none()
    if rel:
        await db.delete(rel)
        await db.commit()
    return rel