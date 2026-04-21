from sqlalchemy import Column, BigInteger, String
from src.db.base_class import Base

class Usuario(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    contrasena = Column(String, unique=True, index=True)