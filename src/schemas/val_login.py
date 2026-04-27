from pydantic import BaseModel

class InicioSesion(BaseModel):
    name: str
    contrasena: str