from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from app.auth.api.deps import require_role, get_current_user
from app.auth.domain.roles import RoleName
from app.auth.domain.models import User

def make_app():
    app = FastAPI()
    @app.get("/admin")
    async def admin_endpoint(_ = Depends(require_role(RoleName.ADMIN))):
        return {"ok": True}
    return app

async def _user_admin():
    return User(id="1", email=None, full_name=None, role="admin", sede_id=None)

async def _user_client():
    return User(id="2", email=None, full_name=None, role="client", sede_id=None)

def test_admin_allows_admin_user():
    app = make_app()
    app.dependency_overrides[get_current_user] = _user_admin
    c = TestClient(app)
    r = c.get("/admin")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

def test_admin_rejects_client_user():
    app = make_app()
    app.dependency_overrides[get_current_user] = _user_client
    c = TestClient(app)
    r = c.get("/admin")
    assert r.status_code == 403
