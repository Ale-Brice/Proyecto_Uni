from sqlalchemy.ext.asyncio import AsyncSession
from src.models.usuarios import Usuario
from sqlalchemy.future import select

async def obtener_usuario_por_nombre(db: AsyncSession, nombre: str, clave_proporcionada: str):
    query = select(Usuario).where(Usuario.name == nombre)

    result = await db.execute(query)

    usuario = result.scalars().first()

    if not usuario:
        return None

    if usuario.hashed_password != clave_proporcionada:
        return None
    return usuario