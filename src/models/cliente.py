from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(BigInteger, primary_key=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    numero = Column(Integer)
    email = Column(String)
    is_active = Column(Boolean, default=True)