from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.cost_adm import registrar_cost_adm, obt_cost_adm, del_cost_adm, up_cost_adm
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker
from src.schemas.val_cost_adm import cost_adm , costadmResponse
from sqlalchemy.future import select
from datetime import date

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/cost_adm/register")
async def register_cost_adm(data: cost_adm, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_cost_adm(db, data.tipo_costo, data.gasto_administrativo, data.fecha)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el costo administrativo")

    return {"message": f"¡Registrado con exito el gasto: {register.gasto_administrativo}!", "status": "success"}

@router.get("/cost_adm", response_model=list[costadmResponse])
async def obtener_cost_adm(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    cost_adm = await obt_cost_adm(db)
    return cost_adm

@router.delete("/cost_adm/{id}")
async def delete_cost_adm(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    cost_adm = await del_cost_adm(db, id)

    if not cost_adm:
        raise HTTPException(status_code=404, detail="Costo administrativo no encontrado")

    return {"Mensaje": "Costo administrativo eliminado con exito"}

@router.put("/cost_adm/{id}")
async def update_cost_adm(id: int, new_tipo_costo : str, new_gasto_administrativo : int , new_fecha : date, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    cost_adm = await up_cost_adm(db, id, new_tipo_costo, new_gasto_administrativo, new_fecha)

    if not cost_adm:
        raise HTTPException(status_code=404, detail="Costo administrativo no encontrado")

    return {"Mensaje": "Costo administrativo actualizado con exito"}