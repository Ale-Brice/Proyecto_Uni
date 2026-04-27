from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text, Integer
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class empleado(Base):
    __tablename__ = "empleado"
    id_empleado = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    numero = Column(Integer, index= True)
    email = Column(String, index=True)
    #usuario_rel = relationship("Usuario", back_populates="empleado_rel")
