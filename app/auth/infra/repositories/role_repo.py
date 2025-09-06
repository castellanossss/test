from app.auth.domain.interfaces import RoleRepository
from app.auth.domain.roles import RoleName

class InMemoryRoleRepo(RoleRepository):
    def __init__(self):
        self._roles: dict[str, RoleName] = {}

    async def get_role(self, user_id: str) -> RoleName:
        return self._roles.get(user_id, "client")

    async def set_role(self, user_id: str, role: RoleName) -> None:
        self._roles[user_id] = role
