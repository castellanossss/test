from pydantic import BaseModel

class AuthMeResponse(BaseModel):
    user: "UserDTO"

from .user import UserDTO
AuthMeResponse.model_rebuild()
