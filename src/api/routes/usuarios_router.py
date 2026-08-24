from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.val_login import InicioSesion
from src.crud.usuarios import *
from src.schemas.val_register import registrar
from src.schemas.get_users import UserResponse
from src.api.deps import crear_token, verificar_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.core.checker import PermissionChecker

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = await obtener_usuario_por_nombre(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario o Clave incorrectos")

    token = crear_token({"sub": user.name})
    return {"message": f"¡Bienvenido {user.name}!", "status": "success", "token": token}

@router.post("/register")
async def register(data: registrar, db: AsyncSession = Depends(get_db), user = Depends(require_create)):
    register = await registrar_usuario(db, data.name, data.contraseña)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el usuario")

    return {"message": f"¡{register.name} Registrado con exito!", "status": "success"}

@router.get("/usuarios", response_model=list[UserResponse])
async def obtener_usuarios(db: AsyncSession = Depends(get_db), user = Depends(require_view)):
    user = await obt_ususarios(db)

    return user

@router.delete("/usuarios/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db), user = Depends(require_delete)):
    user = await delete_user1(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"Mensaje": "Usuario eliminado con exito"}

@router.put("/usuarios/{id}")
async def update_user(id: int, new_name: str, new_password: str, emp_fk: int, db: AsyncSession = Depends(get_db), user = Depends(require_update)):
    user = await up_user(db, id, new_name, new_password, emp_fk)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"Mensaje": "Usuario actualizado con exito"}