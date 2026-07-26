from pydantic import BaseModel

class cost_op(BaseModel):
    tipo_gasto_operativo: str
    gasto_operativo: int

class costopResponse(BaseModel):
    id_costo_oper: int
    tipo_gasto_operativo: str
    cantidad: int

    class Config:
        from_attributes = True