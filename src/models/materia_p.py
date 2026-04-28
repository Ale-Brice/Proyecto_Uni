from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, DECIMAL, Integer, Boolean
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class materia_p(Base):
    __tablename__ = "materia_prima"
    id_materia = Column(BigInteger, primary_key=True)
    tipo_material = Column(String, index=True)
    precio_mat = Column(DECIMAL(10, 2))
    cantidad = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
