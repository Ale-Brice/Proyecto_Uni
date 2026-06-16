from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.clientes import *
from src.db.session import get_db
from src.schemas.val_cliente import cliente, cliResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/cliente/register")
async def register_cliente(data: cliente, db: AsyncSession = Depends(get_db)):
    register = await registrar_cliente(db, data.nombre, data.apellido, data.numero, data.email)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el cliente")

    return {"message": f"¡{register.nombre} Registrado con exito!", "status": "success"}

@router.get("/clientes", response_model=list[cliResponse])
async def obtener_clientes(db: AsyncSession = Depends(get_db)):
    clientes = await obt_clientes(db)
    return clientes

@router.delete("/clientes/{id}")
async def delete_cliente(id: int, db: AsyncSession = Depends(get_db)):
    cliente = await del_cliente(db, id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {"Mensaje": "Cliente eliminado con exito"}

@router.put("/clientes/{id}")
async def update_cliente(id: int, new_name: str, apellido: str, numero: str, email: str, db: AsyncSession = Depends(get_db)):
    cliente = await up_cliente(db, id, new_name, apellido, numero, email)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {"Mensaje": "Cliente actualizado con exito"}