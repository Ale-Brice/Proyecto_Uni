from pydantic import BaseModel

class detalles_pedido(BaseModel):
    fk_pedido: int
    pe_desc: str
    tallas: int
    cantidad: int

class detpedResponse(BaseModel):
    id_detalle_pedido: int
    fk_pedido: int
    pe_desc: str
    tallas: int
    cantidad: int
    is_active: bool

    class Config:
        from_attributes = True