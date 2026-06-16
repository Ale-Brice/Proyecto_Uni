from pydantic import BaseModel

class cliente(BaseModel):
    nombre: str
    apellido: str
    numero: str
    email: str

class cliResponse(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    numero: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True