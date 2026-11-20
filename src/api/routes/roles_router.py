from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.checker import PermissionChecker
from src.crud.roles import *
from src.core.audit import get_audited_db
from src.schemas.val_roles import *
from sqlalchemy.future import select

require_create = PermissionChecker(["crear"])
require_delete = PermissionChecker(["delete"])
require_view = PermissionChecker(["view"])
require_update = PermissionChecker(["update"])

router = APIRouter()

@router.post("/roles/register")
async def register_rol(data: rol, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_rol(db, nombre_rol=data.nombre_rol)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de rol")

    return {"message": f"¡Registrado con exito!", "status": "success"}

@router.get("/roles", response_model=list[rolResponse])
async def obtener_rol(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    rol = await obt_rol(db)
    if not rol:
            raise HTTPException(status_code=400, detail="no se ha encontrado el rol")
    return rol

@router.get("/roles/eliminados", response_model=list[rolResponse])
async def obtener_rol_eliminado(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    rol = await obt_rol_eliminado(db)
    if not rol:
            raise HTTPException(status_code=400, detail="no se ha encontrado el rol")
    return rol

@router.delete("/roles/{id}")
async def delete_rol(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    rol_db = await del_rol(db, id)
    if rol_db == "admin":
        raise HTTPException(status_code=400, detail="No se puede eliminar el rol admin")
    if not rol_db:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"Mensaje": "Rol eliminado con exito"}


@router.post("/roles/{id}/restaurar")
async def restore_rol(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    rol_db = await restaurar_rol(db, id)
    if not rol_db:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"Mensaje": "Rol restaurado con exito"}

@router.post("/permisos/register")
async def register_permiso(data: permiso, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_permiso(db, nombre_permiso=data.nombre_permiso)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de permiso")

    return {"message": f"¡Registrado con exito!", "status": "success"}

@router.get("/permisos", response_model=list[permisoResponse])
async def obtener_permiso(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    permiso = await obt_permiso(db)
    if not permiso:
            raise HTTPException(status_code=400, detail="no se ha encontrado el permiso")
    return permiso

@router.get("/permisos/eliminados", response_model=list[permisoResponse])
async def obtener_permiso_eliminado(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    permiso = await obt_permiso_eliminado(db)
    if not permiso:
            raise HTTPException(status_code=400, detail="no se ha encontrado el permiso")
    return permiso

@router.delete("/permisos/{id}")
async def delete_permiso(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    permiso_db = await del_permiso(db, id)
    if not permiso_db:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return {"Mensaje": "Permiso eliminado con exito"}

@router.post("/permisos/{id}/restaurar")
async def restore_permiso(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    permiso_db = await restaurar_permiso(db, id)
    if not permiso_db:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return {"Mensaje": "Permiso restaurado con exito"}

@router.post("/roles/{id_rol}/permisos/{id_permiso}/asignar")
async def register_permiso_rol(data: permisoRol, db: AsyncSession = Depends(get_audited_db), user = Depends(require_create)):
    register = await registrar_permiso_rol(db, fk_id_rol=data.fk_id_rol, fk_id_permiso=data.fk_id_permiso)

    if not register:
        raise HTTPException(status_code=400, detail="no ha ingresado el detalle de permiso")

    return {"message": f"¡Registrado con exito!", "status": "success"}

@router.get("/permisos/roles", response_model=list[permisoRolResponse])
async def obtener_permiso_rol(db: AsyncSession = Depends(get_audited_db), user = Depends(require_view)):
    permiso_rol = await obt_permiso_rol(db)
    if not permiso_rol:
            raise HTTPException(status_code=400, detail="no se ha encontrado el permiso")
    return permiso_rol

@router.delete("/permisos/roles/{id}")
async def delete_permiso_rol(id: int, db: AsyncSession = Depends(get_audited_db), user = Depends(require_delete)):
    permiso_rol = await del_permiso_rol(db, id)

    if not permiso_rol:
        raise HTTPException(status_code=404, detail="Permiso-rol no encontrado")

    return {"Mensaje": "Permiso-rol eliminado con exito"}

@router.post("/usuarios/roles/asignar")
async def register_rol_usuario(
    data: RolUsuario,
    db: AsyncSession = Depends(get_audited_db),
    user = Depends(require_create)
):
    register = await registrar_rol_usuario(
        db,
        fk_id_usuario=data.fk_id_usuario,
        fk_id_rol=data.fk_id_rol
    )
    if not register:
        raise HTTPException(status_code=400, detail="No se pudo asignar el rol al usuario")
    return {"message": "¡Rol asignado con exito!", "status": "success"}


@router.get("/usuarios/roles", response_model=list[RolUsuarioResponse])
async def obtener_rol_usuario(
    db: AsyncSession = Depends(get_audited_db),
    user = Depends(require_view)
):
    lista = await obt_rol_usuario(db)
    if not lista:
        raise HTTPException(status_code=404, detail="No se encontraron asignaciones de rol-usuario")
    return lista


@router.delete("/usuarios/roles/{id}")
async def delete_rol_usuario(
    id: int,
    db: AsyncSession = Depends(get_audited_db),
    user = Depends(require_delete)
):
    rel = await del_rol_usuario(db, id)
    if not rel:
        raise HTTPException(status_code=404, detail="Asignacion rol-usuario no encontrada")
    return {"Mensaje": "Rol revocado del usuario con exito"}