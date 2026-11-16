from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class empleado(Base):
    __tablename__ = "empleado"
    id_empleado = Column(BigInteger, primary_key=True)
    nombre = Column(String, index=True, nullable=False)
    apellido = Column(String, index=True, nullable=False)
    numero = Column(String(20), nullable=True)
    email = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    #usuario_rel = relationship("Usuario", back_populates="empleado_rel")
