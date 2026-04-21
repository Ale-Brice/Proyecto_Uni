from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime, Table, Text
from src.db.base_class import Base
from datetime import datetime

class Post(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    contrasena = Column(String, index= True)