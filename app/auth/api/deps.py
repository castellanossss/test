from fastapi import Depends, HTTPException, status, Header
from app.auth.domain.interfaces import AuthService
from app.auth.domain.errors import AUTH_INVALID_TOKEN, AUTH_FORBIDDEN
from app.auth.domain.roles import RoleName, has_role
from typing import Callable

def get_auth_service() -> AuthService:
    from app.container import resolve_auth_service
    return resolve_auth_service()

async def get_current_user(
    authorization: str | None = Header(default=None),
    auth: AuthService = Depends(get_auth_service),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_INVALID_TOKEN.message)
    token = authorization.removeprefix("Bearer ").strip()
    try:
        return await auth.resolve_user_from_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_INVALID_TOKEN.message)

def require_role(required: RoleName) -> Callable:
    async def dep(user = Depends(get_current_user)):
        if not has_role(user.role, required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AUTH_FORBIDDEN.message)
        return user
    return dep
