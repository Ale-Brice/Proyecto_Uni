from pydantic import BaseModel
from datetime import datetime, date

class cost_adm(BaseModel):
    tipo_costo: str
    gasto_administrativo: int
    fecha: date

class costadmResponse(BaseModel):
    id_costo_adm: int
    tipo_costo: str
    gasto_administrativo: int
    fecha: date
    is_active: bool

    class Config:
        from_attributes = True

class costadmPartial(BaseModel):
    tipo_costo: str | None = None
    gasto_administrativo: int | None = None
    fecha: date | None = None