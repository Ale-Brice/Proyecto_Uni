from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean, Integer
from src.db.base_class import Base

class detalles_pedido(Base):
    __tablename__ = "detalles_pedido"
    id_detalle_pedido = Column(BigInteger, primary_key=True)
    fk_pedido = Column(BigInteger, ForeignKey("pedido.id_pedido"))
    tallas = Column(Integer)
    cantidad = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
