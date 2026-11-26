from pydantic import BaseModel
from datetime import datetime, date

class cost_op(BaseModel):
    tipo_gasto_operativo: str
    gasto_operativo: float
    fecha: date

class costopResponse(BaseModel):
    id_costo_oper: int
    tipo_gasto_operativo: str
    gasto_operativo: float
    fecha: date
    is_active: bool

    class Config:
        from_attributes = True

class costopPartial(BaseModel):
    tipo_gasto_operativo: str | None = None
    gasto_operativo: float | None = None
    fecha: date | None = None