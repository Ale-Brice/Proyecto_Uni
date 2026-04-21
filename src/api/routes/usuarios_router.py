from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.usuarios import InicioSesion
from src.crud.usuarios import obtener_usuario_por_nombre

router = APIRouter()

@router.post("/login")
def login(data: InicioSesion, db: Session = Depends(get_db)):
    user = obtener_usuario_por_nombre(db, data.name)

    if not user or user.contrasena != data.contrasena:
        raise HTTPException(status_code=400, detail="Usuario o Clave incorrectos")

    return {"message": f"¡Bienvenido {user.name}!", "status": "success"}