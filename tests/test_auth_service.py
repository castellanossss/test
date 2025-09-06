import pytest
import asyncio
from app.auth.domain.services import AuthServiceImpl
from app.auth.domain.interfaces import JWKSClient, UserRepository
from app.auth.domain.models import User

class FakeJWKS(JWKSClient):
    async def get_signing_keys(self) -> dict:
        return {"keys": []}
    async def decode_and_verify(self, token: str, audience: str | None = None, issuer: str | None = None) -> dict:
        return {
            "sub": "user_fake",
            "email": "fake@example.com",
            "given_name": "Fake",
            "family_name": "User",
            "role": "client",
        }

class InMemUserRepo(UserRepository):
    def __init__(self):
        self._data: dict[str, User] = {}
    async def get(self, user_id: str) -> User | None:
        return self._data.get(user_id)
    async def upsert(self, user: User) -> User:
        self._data[user.id] = user
        return user
    async def delete(self, user_id: str) -> None:
        self._data.pop(user_id, None)

@pytest.mark.asyncio
async def test_auth_service_resolve_and_upsert():
    jwks = FakeJWKS()
    repo = InMemUserRepo()
    svc = AuthServiceImpl(jwks, repo)

    user = await svc.resolve_user_from_token("any-token")
    assert user.id == "user_fake"
    assert user.email == "fake@example.com"
    assert user.full_name == "Fake User"

    # upsert ejecutado
    stored = await repo.get("user_fake")
    assert stored is not None
    assert stored.email == "fake@example.com"
