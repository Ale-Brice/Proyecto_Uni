from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.db.session import get_db
from src.api.deps import get_current_user

async def get_audited_db(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user:
        await db.execute(
            text("SELECT set_config('app.current_user_id', :user_id, true)"),
            {"user_id": str(current_user.name)}
        )
    return db