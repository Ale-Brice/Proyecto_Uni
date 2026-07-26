from pydantic import BaseModel

class pedido(BaseModel):
    fk_cliente: int
    fk_producto: int

class pedResponse(BaseModel):
    id_pedido: int
    fk_cliente: int
    fk_producto: int
    is_active: bool

    class Config:
        from_attributes = True