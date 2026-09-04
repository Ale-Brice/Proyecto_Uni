from pydantic import BaseModel
from datetime import datetime, date

class materia_p(BaseModel):
    tipo_material: str
    precio_mat: float
    cantidad: int
    fecha: date

class matResponse(BaseModel):
    id_materia: int
    tipo_material: str
    precio_mat: float
    cantidad: int
    fecha: date
    is_active: bool

    class Config:
        from_attributes = True