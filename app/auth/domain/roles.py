from enum import Enum

class RoleName(str, Enum):
    CLIENT = "client"
    TRAINER = "trainer"
    ADMIN = "admin"

def has_role(user_role: str, required: RoleName) -> bool:
    return user_role == required.value or (user_role == "admin" and required != RoleName.ADMIN)
