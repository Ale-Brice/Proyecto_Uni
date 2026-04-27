from sqlalchemy import Column, BigInteger, String, ForeignKey
from src.db.base_class import Base

class pedido(Base):
    __tablename__ = "pedido"
    id_pedido = Column(BigInteger, primary_key=True, index=True)
    fk_cliente = Column(BigInteger, ForeignKey("cliente.id_cliente"))
    pe_desc = Column(String, unique=True, index=True)
    fk_producto = Column(BigInteger, ForeignKey("producto.id_producto"))
    cantidad = Column(String, unique=True, index=True)
