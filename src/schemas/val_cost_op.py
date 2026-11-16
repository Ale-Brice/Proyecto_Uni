from pydantic import BaseModel
from datetime import datetime, date

class cost_op(BaseModel):
    tipo_gasto_operativo: str
    gasto_operativo: int
    fecha: date

class costopResponse(BaseModel):
    id_costo_oper: int
    tipo_gasto_operativo: str
    gasto_operativo: int
    fecha: date
    is_active: bool

    class Config:
        from_attributes = True

class costopPartial(BaseModel):
    tipo_gasto_operativo: str | None = None
    gasto_operativo: int | None = None
    fecha: date | None = None