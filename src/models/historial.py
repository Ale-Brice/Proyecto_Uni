from sqlalchemy import Column, BigInteger, String, ForeignKey
from src.db.base_class import Base

class historial_ped(Base):
    __tablename__ = "historial_ped"
    id_historial_ped = Column(BigInteger, primary_key=True, index=True)
    id_pedido = Column(BigInteger, primary_key=True, index=True)
    cliente = Column(String, unique=True, index=True)
    pe_desc = Column(String, unique=True, index=True)
    producto = Column(String, unique=True, index=True)


    cantidad = Column(String, unique=True, index=True)

