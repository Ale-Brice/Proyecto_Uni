from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    empleado_fk: int | None = None

    class Config:
        from_attributes = True

class User(BaseModel):
    name: str
    is_active: bool | None = None


class UserInDB(User):
    hashed_password: str