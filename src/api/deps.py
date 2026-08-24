import jwt
from datetime import datetime, timedelta
from src.core.config import settings
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from src.schemas.token import TokenData
from src.db.session import get_db
from src.schemas.get_users import UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Usuario, rol, rol_usuario, permiso, permiso_rol
from sqlalchemy.future import select

security = HTTPBearer()

def crear_token(data: dict):
    datos = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expire})
    token = jwt.encode(datos, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("El token ha expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")

async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extraemos el string del token del objeto credentials
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        name = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user(db, name=token_data.name)
    if user is None:
        raise credentials_exception

    return user

async def get_user(db: AsyncSession, name: str):
    result = await db.execute(select(Usuario).where(Usuario.name == name))
    return result.scalars().first()

async def get_user_permissions(db: AsyncSession, user_id: int) -> list[str]:
    # Hacemos múltiples JOINs para llegar desde el usuario hasta los nombres de los permisos
    stmt = (
        select(permiso.nombre_permiso)
        .join(permiso_rol, permiso.id_permiso == permiso_rol.fk_id_permiso)
        .join(rol, permiso_rol.fk_id_rol == rol.id_rol)
        .join(rol_usuario, rol.id_rol == rol_usuario.fk_id_rol)
        .where(rol_usuario.fk_id_usuario == user_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()