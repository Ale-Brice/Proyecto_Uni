from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from src.models.usuarios import Usuario
from sqlalchemy.future import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def obtener_usuario_por_nombre(db: AsyncSession, nombre: str, clave_proporcionada: str):
    query = select(Usuario).where(Usuario.name == nombre)

    result = await db.execute(query)

    usuario = result.scalars().first()

    if not usuario:
        return None

    is_valid = pwd_context.verify(clave_proporcionada, usuario.hashed_password)

    if not is_valid:
        return None
    return usuario

async def registrar_usuario(db: AsyncSession, nombre: str, clave_proporcionada: str):
    if not nombre or not clave_proporcionada:
        return None

    hashed_password = pwd_context.hash(clave_proporcionada)
    new_user = Usuario(name=nombre, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def delete_user1(db: AsyncSession, id):
    user = await db.get(Usuario, id)

    if not user:
        return user

    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user