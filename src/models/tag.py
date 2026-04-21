from sqlalchemy import Column, BigInteger, String
from src.db.base_class import Base

class tag(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)