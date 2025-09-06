# app/container.py
from app.auth.domain.services import AuthServiceImpl
from app.auth.infra.jwks_client import HTTPJWKSClient
from app.auth.infra.repositories.user_repo_sql import SqlUserRepo

def resolve_auth_service():
    jwks = HTTPJWKSClient()
    user_repo = SqlUserRepo()
    return AuthServiceImpl(jwks, user_repo)
