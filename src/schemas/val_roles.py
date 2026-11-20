from pydantic import BaseModel

class rol(BaseModel):
    nombre_rol: str

class rolResponse(BaseModel):
    id_rol: int
    nombre_rol: str
    is_active: bool

    class Config:
        from_attributes = True

class rolPartial(BaseModel):
    nombre_rol: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

class permiso(BaseModel):
    nombre_permiso: str

class permisoResponse(BaseModel):
    id_permiso: int
    nombre_permiso: str
    is_active: bool

    class Config:
        from_attributes = True

class permisoPartial(BaseModel):
    nombre_permiso: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

class permisoRol(BaseModel):
    fk_id_rol: int
    fk_id_permiso: int

class permisoRolResponse(BaseModel):
    id_permiso_rol: int
    fk_id_rol: int
    fk_id_permiso: int
    is_active: bool

    class Config:
        from_attributes = True

class permisoRolPartial(BaseModel):
    nombre_permiso: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

class RolUsuario(BaseModel):
    fk_id_usuario: int
    fk_id_rol: int

class RolUsuarioResponse(BaseModel):
    id_rol_user: int
    fk_id_usuario: int
    fk_id_rol: int
    is_active: bool

    class Config:
        from_attributes = True

class RolUsuarioPartial(BaseModel):
    fk_id_usuario: int | None = None
    fk_id_rol: int | None = None
    is_active: bool

    class Config:
        from_attributes = True