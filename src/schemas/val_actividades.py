from pydantic import BaseModel
from datetime import datetime, date

class actividad(BaseModel):
    fk_empleado: int
    fk_pedido: int
    descripcion_tarea: str
    fecha_inicio: datetime
    fecha_final : datetime

class actResponse(BaseModel):
    id_actividad: int
    fk_empleado: int
    fk_pedido: int
    descripcion_tarea: str
    fecha_inicio: datetime
    fecha_final : datetime
    is_active: bool

    class Config:
        from_attributes = True