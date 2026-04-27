from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class producto(Base):
    __tablename__ = "producto"
    id_producto = Column(BigInteger, primary_key=True, index=True)
    nombre_p = Column(String, unique=True, index=True)
    tipo_p = Column(String, unique=True, index=True)
    detalle_p = Column(String, index=True)
    precio_p = Column(String, unique=True, index=True)
