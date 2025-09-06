from abc import ABC, abstractmethod
from typing import Protocol, Optional
from .models import User
from .roles import RoleName

# ---- JWKS / Token ----
class JWKSClient(Protocol):
    async def get_signing_keys(self) -> dict: ...
    async def decode_and_verify(self, token: str, audience: str, issuer: str) -> dict: ...

# ---- Services ----
class AuthService(ABC):
    @abstractmethod
    async def resolve_user_from_token(self, bearer_token: str) -> User: ...
    @abstractmethod
    async def upsert_from_claims(self, claims: dict) -> User: ...

class UserService(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]: ...
    @abstractmethod
    async def upsert(self, user: User) -> User: ...
    @abstractmethod
    async def set_role(self, user_id: str, role: RoleName) -> None: ...

# ---- Repositories ----
class UserRepository(ABC):
    @abstractmethod
    async def get(self, user_id: str) -> Optional[User]: ...
    @abstractmethod
    async def upsert(self, user: User) -> User: ...

class RoleRepository(ABC):
    @abstractmethod
    async def get_role(self, user_id: str) -> RoleName: ...
    @abstractmethod
    async def set_role(self, user_id: str, role: RoleName) -> None: ...

class AuditRepository(ABC):
    @abstractmethod
    async def log_event(self, actor_id: str | None, action: str, data: dict | None = None) -> None: ...
