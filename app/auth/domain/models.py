from dataclasses import dataclass
from typing import Optional, Literal

RoleName = Literal["client", "trainer", "admin"]

@dataclass
class User:
    id: str
    email: Optional[str]
    full_name: Optional[str]
    role: RoleName
    sede_id: Optional[int]
