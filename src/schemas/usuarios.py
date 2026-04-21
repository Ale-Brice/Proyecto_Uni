from pydantic import BaseModel

class inicio_sesion(BaseModel):
    name: str
    contrasena: str