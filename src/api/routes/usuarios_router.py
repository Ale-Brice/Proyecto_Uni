from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.val_login import InicioSesion
from src.crud.usuarios import obtener_usuario_por_nombre

router = APIRouter()

@router.post("/login")
async def login(data: InicioSesion, db: AsyncSession = Depends(get_db)):
    user = await obtener_usuario_por_nombre(db, data.name, data.contrasena)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario o Clave incorrectos")

    return {"message": f"¡Bienvenido {user.name}!", "status": "success"}