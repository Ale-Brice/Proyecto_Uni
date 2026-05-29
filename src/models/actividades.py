from sqlalchemy import Column, BigInteger, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class actividad(Base):
    __tablename__ = "actividad"
    id_actividad = Column(BigInteger, primary_key=True)
    fk_empleado = Column(BigInteger, ForeignKey("empleado.id_empleado"))
    fk_pedido = Column(BigInteger, ForeignKey("pedido.id_pedido"))
    descripcion_tarea = Column(String, index=True)
    fecha_inicio = Column(DateTime, index=True)
    fecha_final = Column(DateTime, index=True)
    is_active = Column(Boolean, default=True)
