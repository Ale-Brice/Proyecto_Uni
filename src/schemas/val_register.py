from pydantic import BaseModel

class registrar(BaseModel):
    name: str
    contraseña: str