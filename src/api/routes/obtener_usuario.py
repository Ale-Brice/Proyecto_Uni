from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.crud.obtener_usuario import obt_ususarios
from src.schemas.get_users import UserResponse

router = APIRouter()

@router.get("/usuarios", response_model=list[UserResponse])
async def obtener_usuarios(db: AsyncSession = Depends(get_db)):
    user = await obt_ususarios(db)

    return user