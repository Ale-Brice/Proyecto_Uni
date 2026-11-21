from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.audit import get_audited_db
from src.api.deps import get_current_user
from src.api.deps import get_user_permissions

class PermissionChecker:
    def __init__(self, required_permissions: list[str], require_all: bool = False):
        self.required_permissions = required_permissions
        self.require_all = require_all

    async def __call__(self, current_user=Depends(get_current_user)):
        user_permissions = set(current_user.permissions or [])

        if self.require_all:
            missing = [p for p in self.required_permissions if p not in user_permissions]
            if missing:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permiso denegado: requieres '{missing[0]}'."
                )
        else:
            if not any(p in user_permissions for p in self.required_permissions):
                perms_str = " o ".join(f"'{p}'" for p in self.required_permissions)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permiso denegado: requieres {perms_str}."
                )

        return current_user