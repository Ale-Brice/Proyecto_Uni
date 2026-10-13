from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.clientes import *
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker
from src.schemas.val_cliente import *
from sqlalchemy.future import select

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/clientes/register")
async def register_cliente(data: cliente, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_cliente(db, data.nombre, data.apellido, data.numero, data.email)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el cliente")

    return {"message": f"¡{register.nombre} Registrado con exito!", "status": "success"}

@router.get("/clientes", response_model=list[cliResponse])
async def obtener_clientes(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    clientes = await obt_clientes(db)
    return clientes

@router.delete("/clientes/{id}")
async def delete_cliente(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    cliente = await del_cliente(db, id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {"Mensaje": "Cliente eliminado con exito"}

@router.put("/clientes/{id}")
async def update_cliente(id: int, new_name: str, apellido: str, numero: str, email: str, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    cliente = await up_cliente(db, id, new_name, apellido, numero, email)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {"Mensaje": "Cliente actualizado con exito"}

@router.patch("/clientes/{id}")
async def update_cliente_parcial(id: int, cli_data: cliPartial, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    update_data = cli_data.model_dump(exclude_unset=True)

    cli = await update_clienteP(
        db=db,
        id=id,
        nombre=update_data.get("nombre"),
        apellido=update_data.get("apellido"),
        numero=update_data.get("numero"),
        email=update_data.get("email")
    )
    if not cli:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {"Mensaje": "Cliente actualizado con exito"}