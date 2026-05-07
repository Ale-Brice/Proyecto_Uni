from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.val_register import registrar
from src.crud.registrar import registrar_usuario

router = APIRouter()

@router.post("/register")
async def register(data: registrar, db: AsyncSession = Depends(get_db)):
    register = await registrar_usuario(db, data.name, data.contraseña)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el usuario")

    return {"message": f"¡{register.name} Registrado con exito!", "status": "success"}
