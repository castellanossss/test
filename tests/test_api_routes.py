from fastapi import Depends
from app.auth.api.deps import get_auth_service
from app.auth.domain.interfaces import AuthService
from app.auth.domain.models import User

class FakeAuthService(AuthService):
    async def resolve_user_from_token(self, bearer_token: str) -> User:
        return User(id="u_test", email="t@e.com", full_name="Tester", role="client", sede_id=None)
    async def upsert_from_claims(self, claims: dict) -> User:
        return User(id="u_test", email="t@e.com", full_name="Tester", role="client", sede_id=None)

def override_auth_service():
    return FakeAuthService()

def test_health(test_client):
    r = test_client.get("/auth/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

def test_me_unauthorized_without_token(test_client):
    r = test_client.get("/auth/me")
    assert r.status_code == 401

def test_me_ok_with_bearer_and_override(test_client):
    from app.main import app
    app.dependency_overrides[get_auth_service] = override_auth_service

    r = test_client.get("/auth/me", headers={"Authorization": "Bearer ANY"})
    assert r.status_code == 200
    body = r.json()
    assert body["user"]["id"] == "u_test"
    assert body["user"]["email"] == "t@e.com"

    app.dependency_overrides.clear()
