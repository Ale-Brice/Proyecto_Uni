from pydantic import BaseModel
from datetime import datetime, date

class actividad(BaseModel):
    fk_empleado: int
    fk_pedido: int
    descripcion_tarea: str
    fecha_inicio: date
    fecha_final : date

class actResponse(BaseModel):
    id_actividad: int
    fk_empleado: int
    fk_pedido: int
    descripcion_tarea: str
    fecha_inicio: date
    fecha_final : date
    is_active: bool

    class Config:
        from_attributes = True