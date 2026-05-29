from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Usuario
from sqlalchemy.future import select

async def obt_ususarios(db: AsyncSession, ):
    query = select(Usuario).where(Usuario.is_active == True)

    result = await db.execute(query)

    usuario = result.scalars().all()
    return usuario