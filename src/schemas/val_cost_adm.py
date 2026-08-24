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

    class Config:
        from_attributes = True