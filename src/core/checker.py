from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.audit import get_audited_db
from src.api.deps import get_current_user
from src.api.deps import get_user_permissions

class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    async def __call__(self, current_user = Depends(get_current_user)):
        for req_permission in self.required_permissions:
            if req_permission not in current_user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permiso denegado: requieres '{req_permission}'."
                )
        return current_user