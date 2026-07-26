from pydantic import BaseModel, ConfigDict

class IgnoredType:
    pass

class det_pro(BaseModel):
    fk_producto : int
    tallas: str
    cantidad: int

class detproResponse(BaseModel):
    id_det_pro: int
    tallas: str
    cantidad: int
    fk_producto: int

    class Config:
        from_attributes = True