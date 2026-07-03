from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.materia_p import *
from src.db.session import get_db
from src.schemas.val_materia_p import materia_p, matResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/materia_prima/register")
async def register_materia_p(data: materia_p, db: AsyncSession = Depends(get_db)):
    register = await registrar_materia_p(db, data.tipo_material, data.precio_mat, data.cantidad)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado la materia prima")

    return {"message": f"¡{register.tipo_material} Registrado con exito!", "status": "success"}

@router.get("/materia_prima", response_model=list[matResponse])
async def obtener_materia_p(db: AsyncSession = Depends(get_db)):
    mat = await obt_materia_p(db)
    return mat

@router.delete("/materia_prima/{id}")
async def delete_materia_p(id: int, db: AsyncSession = Depends(get_db)):
    materia_p = await del_materia_p(db, id)

    if not materia_p:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    return {"Mensaje": "Materia prima eliminada con exito"}

@router.put("/materia_prima/{id}")
async def update_materia_p(id: int, new_tipo_material: str, new_precio_mat: float, new_cantidad: int, db: AsyncSession = Depends(get_db)):
    materia_p = await up_materia_p(db, id, new_tipo_material, new_precio_mat, new_cantidad)

    if not materia_p:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    return {"Mensaje": "Materia prima actualizada con exito"}