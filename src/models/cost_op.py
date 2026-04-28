from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class cost_op(Base):
    __tablename__ = "cost_op"
    id_materia = Column(BigInteger, primary_key=True)
    corte = Column(String, index=True)
    confeccion = Column(String, index=True)
    ojal = Column(String, index=True)
    bordado = Column(String, index=True)
    sublimado = Column(String, index=True)
    plancha = Column(String, index=True)
    plancha_ter = Column(String, index=True)
    diseño = Column(String, index=True)
    montaje = Column(String, index=True)

class cost_adm(Base):
    __tablename__ = "cost_adm"
    id_materia = Column(BigInteger, primary_key=True)
    impuestos = Column(String, index=True)
    alquiler = Column(String, index=True)
    gastos_adm = Column(String, index=True)
    publicidad = Column(String, index=True)
    gasolina = Column(String, index=True)
    moto_taxi = Column(String, index=True)
