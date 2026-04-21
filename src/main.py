from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.usuarios import Usuario
from src.core.config import settings
from src.schemas.usuarios import inicio_sesion
from src.db import base

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

@app.post("/login")
def login(data: inicio_sesion, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.name == data.name).first()

    if not user or user.contrasena != data.contrasena:
        raise HTTPException(status_code=400, detail="Usuario o Clave incorrectos")

    return {"message": f"¡Bienvenido {user.name}!", "status": "success"}