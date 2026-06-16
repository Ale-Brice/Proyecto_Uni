from pydantic import BaseModel

class empleado(BaseModel):
    nombre: str
    apellido: str
    numero: str
    email: str

class EmpResponse(BaseModel):
    id_empleado: int
    nombre: str
    apellido: str
    numero: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True