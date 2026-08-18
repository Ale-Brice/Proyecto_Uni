from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(50), nullable=False, index=True)
    action = Column(String(10), nullable=False)  # 'INSERT', 'UPDATE', 'DELETE'
    old_data = Column(JSONB, nullable=True)
    new_data = Column(JSONB, nullable=True)
    changed_by = Column(String(100), nullable=True, index=True)  # ID o email del usuario
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)