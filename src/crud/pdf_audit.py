from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.AuditLog import AuditLog

async def obt_audit_log_mes(db: AsyncSession, year: int, month: int):
    query = select(AuditLog).where(
        extract('year', AuditLog.created_at) == year,
        extract('month', AuditLog.created_at) == month
    ).order_by(AuditLog.created_at.asc())

    result = await db.execute(query)
    return result.scalars().all()