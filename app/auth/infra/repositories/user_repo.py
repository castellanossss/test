from app.auth.domain.interfaces import UserRepository
from app.auth.domain.models import User

class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self._data: dict[str, User] = {}

    async def get(self, user_id: str) -> User | None:
        return self._data.get(user_id)

    async def upsert(self, user: User) -> User:
        self._data[user.id] = user
        return user
