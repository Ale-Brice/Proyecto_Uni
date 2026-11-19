from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.detalles_producto import *
from src.core.audit import get_audited_db
from src.core.checker import PermissionChecker
from src.schemas.val_detalle_pro import *
from sqlalchemy.future import select

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/detalle_pro/register")
async def register_detalle_producto(data: det_pro, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_detalle_pro(db, data.tallas, data.cantidad, data.fk_producto)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de producto")

    return {"message": f"¡{register.tallas} Registrado con exito!", "status": "success"}

@router.get("/detalle_pro", response_model=list[detproResponse])
async def obtener_detalle_producto(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    det_pro = await obt_detalle_pro(db)
    if not det_pro:
            raise HTTPException(status_code=400, detail="no se encontraron detalles de producto")
    return det_pro

@router.delete("/detalle_pro/{id}")
async def delete_detalle_producto(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    detalle_ped = await del_detalle_pro(db, id)

    if not detalle_ped:
        raise HTTPException(status_code=404, detail="Detalle de producto no encontrado")

    return {"Mensaje": "Detalle de producto eliminado con exito"}

@router.put("/detalle_pro/{id}")
async def update_detalle_producto(id: int, data: det_pro, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    detalle_pro = await up_detalle_pro(db, id, data.tallas, data.cantidad, data.fk_producto)

    if not detalle_pro:
        raise HTTPException(status_code=404, detail="Detalle de producto no encontrado")

    return {"Mensaje": "Detalle de producto actualizado con exito"}

@router.patch("/detalle_pro/{id}")
async def update_detalle_producto_parcial(id: int, det_data: detproPartial, db: AsyncSession = Depends(get_audited_db), user = Depends(require_update)):
    update_data = det_data.model_dump(exclude_unset=True)

    det = await update_detalle_pro(
        db=db,
        id=id,
        tallas=update_data.get("tallas"),
        cantidad=update_data.get("cantidad"),
        fk_producto=update_data.get("fk_producto")
    )
    if not det:
        raise HTTPException(status_code=404, detail="Detalle de producto no encontrado")

    return {"Mensaje": "Detalle de producto actualizado con exito"}

@router.get("/detalle_pro/eliminados", response_model=list[detproResponse])
async def obtener_detalle_producto_eliminados(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    det_pro = await obt_detalle_pro_eliminados(db)
    if not det_pro:
            raise HTTPException(status_code=400, detail="no se encontraron detalles de producto eliminados")
    return det_pro

@router.post("/detalle_pro/{id}/restaurar")
async def restaurar_detalle_producto(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    detalle_ped = await rest_detalle_pro(db, id)

    if not detalle_ped:
        raise HTTPException(status_code=404, detail="Detalle de producto no encontrado")

    return {"Mensaje": "Detalle de producto restaurado con exito"}