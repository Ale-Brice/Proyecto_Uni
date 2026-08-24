from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.audit import get_audited_db
from src.api.deps import get_current_user
from src.api.deps import get_user_permissions

class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        # Ahora recibimos una lista de permisos necesarios
        self.required_permissions = required_permissions

    async def __call__(
        self,
        db: AsyncSession = Depends(get_audited_db), 
        current_user = Depends(get_current_user)
    ):
        # 1. Obtenemos TODOS los permisos que tiene el usuario actual
        user_permissions = await get_user_permissions(db, current_user.id)
        # 2. Verificamos si el usuario tiene TODOS los permisos requeridos para el endpoint
        for req_permission in self.required_permissions:
            if req_permission not in user_permissions:
                # Si le falta al menos uno, bloqueamos el acceso
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permiso denegado: requieres '{req_permission}' para esta acción."
                )
        return current_user