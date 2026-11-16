from sqlalchemy import Boolean, Column, BigInteger, Date, ForeignKey, String, DateTime, Table, Text, DECIMAL, Integer, Boolean
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class ventas(Base):
    __tablename__ = "ventas"
    id_ventas = Column(BigInteger, primary_key=True)
    fk_producto = Column(BigInteger, ForeignKey("producto.id_producto"))
    precio_p = Column(DECIMAL(10, 2))
    cantidad = Column(Integer, default=0)
    fecha = Column(Date, index=True)
    is_active = Column(Boolean, default=True)