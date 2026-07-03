import jwt
from datetime import datetime, timedelta
from src.core.config import settings

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