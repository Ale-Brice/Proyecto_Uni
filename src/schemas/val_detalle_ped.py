from pydantic import BaseModel

class detalles_pedido(BaseModel):
    tallas: int
    cantidad: int

class detpedResponse(BaseModel):
    id_detalle_pedido: int
    tallas: int
    cantidad: int
    is_active: bool

    class Config:
        from_attributes = True