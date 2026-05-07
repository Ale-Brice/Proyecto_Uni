from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Usuario
from sqlalchemy.future import select

async def registrar_usuario(db: AsyncSession, nombre: str, clave_proporcionada: str):
    new_user = Usuario(name=nombre, hashed_password=clave_proporcionada)

    db.add(new_user)
    await db.commit()
    db.refresh(new_user)
    return new_user