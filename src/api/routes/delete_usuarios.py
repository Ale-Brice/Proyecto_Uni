from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.db.base import *
from src.crud.usuarios import delete_user1

router = APIRouter()

@router.delete("/usuarios/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await delete_user1(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"Mensaje": "Usuario eliminado con exito"}