from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer, DECIMAL
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class cost_op(Base):
    __tablename__ = "cost_op"
    id_costo_oper = Column(BigInteger, primary_key=True)
    tipo_gasto_operativo = Column(String, index=True)
    gasto_operativo = Column(DECIMAL(10, 2))

class cost_adm(Base):
    __tablename__ = "cost_adm"
    id_costo_adm = Column(BigInteger, primary_key=True)
    tipo_costo = Column(String, index=True)
    gasto_administrativo = Column(DECIMAL(10, 2))
