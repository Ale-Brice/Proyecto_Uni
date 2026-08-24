from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.empleados import *
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker
from src.schemas.val_empleado import empleado, EmpResponse
from sqlalchemy.future import select

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/empleado/register")
async def register_empleado(data: empleado, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_empleado(db, data.nombre, data.apellido, data.numero, data.email)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el empleado")

    return {"message": f"¡{register.nombre} Registrado con exito!", "status": "success"}

@router.get("/empleados", response_model=list[EmpResponse])
async def obtener_empleados(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    emp = await obt_empleados(db)
    return emp

@router.delete("/empleados/{id}")
async def delete_empleado(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    emp = await del_empleado(db, id)

    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return {"Mensaje": "Empleado eliminado con exito"}

@router.put("/empleados/{id}")
async def update_empleado(id: int, new_name: str, apellido: str, numero: str, email: str, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    emp = await up_empleado(db, id, new_name, apellido, numero, email)

    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return {"Mensaje": "Empleado actualizado con exito"}