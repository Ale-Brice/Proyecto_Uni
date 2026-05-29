from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class detalle_pro(Base):
    __tablename__ = "detalle_pro"
    id_det_pro = Column(BigInteger, primary_key=True)
    tallas = Column(String, index=True)
    cantidad_talla = Column(Integer, default=0)
    fk_producto = Column(BigInteger, ForeignKey("producto.id_producto"))
