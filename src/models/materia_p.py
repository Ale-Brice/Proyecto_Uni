from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class materia_p(Base):
    __tablename__ = "materia_prima"
    id_materia = Column(BigInteger, primary_key=True, index=True)
    telas = Column(String, index=True)
    forro = Column(String, index=True)
    guata = Column(String, index=True)
    malla = Column(String, index=True)
    pelon = Column(String, index=True)
    entretela = Column(String, index=True)
    elastico = Column(String, index=True)
    hilo = Column(String, index=True)
    cierres = Column(String, index=True)
    hebillas = Column(String, index=True)
    botones = Column(String, index=True)
    bolsas = Column(String, index=True)
