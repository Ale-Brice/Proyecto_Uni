from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.val_login import InicioSesion
from src.crud.usuarios import obtener_usuario_por_nombre
from src.schemas.val_register import registrar
from src.crud.usuarios import registrar_usuario

router = APIRouter()

@router.post("/login")
async def login(data: InicioSesion, db: AsyncSession = Depends(get_db)):
    user = await obtener_usuario_por_nombre(db, data.name, data.contrasena)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario o Clave incorrectos")

    return {"message": f"¡Bienvenido {user.name}!", "status": "success"}

@router.post("/register")
async def register(data: registrar, db: AsyncSession = Depends(get_db)):
    register = await registrar_usuario(db, data.name, data.contraseña)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el usuario")

    return {"message": f"¡{register.name} Registrado con exito!", "status": "success"}