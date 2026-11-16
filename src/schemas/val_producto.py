from pydantic import BaseModel

class producto(BaseModel):
    nombre_p: str
    tipo_p: str
    precio_p: float

class proResponse(BaseModel):
    id_producto: int
    nombre_p: str
    tipo_p: str
    precio_p: float
    is_active: bool

    class Config:
        from_attributes = True

class proPartial(BaseModel):
    nombre_p: str | None = None
    tipo_p: str | None = None
    precio_p: float | None = None