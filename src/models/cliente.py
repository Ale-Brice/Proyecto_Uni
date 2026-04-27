from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    numero = Column(Integer, index= True)
    email = Column(String, index=True)
    fk_pedido = Column(BigInteger, ForeignKey("pedido.id_pedido"))