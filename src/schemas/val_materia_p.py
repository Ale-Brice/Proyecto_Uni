from pydantic import BaseModel

class materia_p(BaseModel):
    tipo_material: str
    precio_mat: float
    cantidad: int

class matResponse(BaseModel):
    id_materia: int
    tipo_material: str
    precio_mat: float
    cantidad: int
    is_active: bool

    class Config:
        from_attributes = True