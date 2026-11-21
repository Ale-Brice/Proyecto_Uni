from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.pdf_audit import *
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker
from src.schemas.val_actividades import *
from sqlalchemy.future import select

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_view_actividades = PermissionChecker(["view_actividades"])
require_update = PermissionChecker(["update"])

require_view_act = PermissionChecker(["view", "view_actividades"])

router = APIRouter()

@router.get("/auditoria")
async def obtener_actividad(db: AsyncSession = Depends(get_audited_db)):
    act = await obt_audit_log(db)
    if not act:
            raise HTTPException(status_code=400, detail="no se encontraron actividades")
    return act