from pydantic import BaseModel
from datetime import datetime, date

class venta(BaseModel):
    fk_producto: int
    precio_p: float
    cantidad: int
    fecha: date

class ventaResponse(BaseModel):
    id_ventas: int
    fk_producto: int
    precio_p: float
    cantidad: int
    fecha: date
    is_active: bool

    class Config:
        from_attributes = True

class ventaPartial(BaseModel):
    fk_producto: int | None = None
    precio_p: float | None = None
    cantidad: int | None = None
    fecha: date | None = None