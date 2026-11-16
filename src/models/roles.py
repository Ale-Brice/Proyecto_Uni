from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class rol(Base):
    __tablename__ = "rol"
    id_rol = Column(BigInteger, primary_key=True)
    nombre_rol = Column(String, unique=True, index=True)
    creado_en = Column(DateTime, index=True)
    actualizad_en = Column(DateTime, index=True)

class rol_usuario(Base):
    __tablename__ = "rol_usuario"
    id_rol_user = Column(BigInteger, primary_key=True)
    fk_id_usuario = Column(BigInteger, ForeignKey("users.id"))
    fk_id_rol = Column(BigInteger, ForeignKey("rol.id_rol"))
    creado_en = Column(DateTime, index=True)
    actualizad_en = Column(DateTime, index=True)

class permiso(Base):
    __tablename__ = "permiso"
    id_permiso = Column(BigInteger, primary_key=True)
    nombre_permiso = Column(String, unique=True, index=True)
    creado_en = Column(DateTime, index=True)
    actualizad_en = Column(DateTime, index=True)

class permiso_rol(Base):
    __tablename__ = "permiso_rol"
    id_permiso_rol = Column(BigInteger, primary_key=True)
    fk_id_rol = Column(BigInteger, ForeignKey("rol.id_rol"))
    fk_id_permiso = Column(BigInteger, ForeignKey("permiso.id_permiso"))
    creado_en = Column(DateTime, index=True)
    actualizad_en = Column(DateTime, index=True)