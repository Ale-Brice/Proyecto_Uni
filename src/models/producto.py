from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, DECIMAL, Integer, Boolean
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class producto(Base):
    __tablename__ = "producto"
    id_producto = Column(BigInteger, primary_key=True)
    nombre_p = Column(String, index=True)
    tipo_p = Column(String, index=True)
    detalle_p = Column(String)
    precio_p = Column(DECIMAL(10, 2))
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
