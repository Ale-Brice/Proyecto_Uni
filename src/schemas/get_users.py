from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    empleado_fk: int | None = None

    class Config:
        from_attributes = True