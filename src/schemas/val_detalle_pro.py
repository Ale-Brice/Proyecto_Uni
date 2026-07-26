from pydantic import BaseModel

class det_pro(BaseModel):
    fk_producto : int
    cantidad: int
    talla: str

class detproResponse(BaseModel):
    id_det_pro = int
    tallas = str
    cantidad_talla = int
    fk_producto = int

    class Config:
        from_attributes = True