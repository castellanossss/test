from pydantic import BaseModel, EmailStr
from typing import Literal

RoleName = Literal["client", "trainer", "admin"]

class RoleDTO(BaseModel):
    name: RoleName

class UserDTO(BaseModel):
    id: str
    email: EmailStr | None = None
    full_name: str | None = None
    role: RoleName
    sede_id: int | None = None
