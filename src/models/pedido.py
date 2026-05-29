from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean, Integer
from src.db.base_class import Base

class pedido(Base):
    __tablename__ = "pedido"
    id_pedido = Column(BigInteger, primary_key=True)
    fk_cliente = Column(BigInteger, ForeignKey("cliente.id_cliente"))
    pe_desc = Column(String)
    fk_producto = Column(BigInteger, ForeignKey("producto.id_producto"))
    cantidad = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
