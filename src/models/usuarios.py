from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class Usuario(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    empleado_fk = Column(BigInteger, ForeignKey("empleado.id_empleado"), nullable=True, unique=True)
    is_active = Column(Boolean, default=True)
