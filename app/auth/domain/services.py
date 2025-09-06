# app/auth/domain/services.py
from app.auth.domain.interfaces import AuthService, UserRepository, JWKSClient
from app.auth.domain.models import User
from app.auth.infra.mappers.user_mapper import from_claims

class AuthServiceImpl(AuthService):
    def __init__(self, jwks_client: JWKSClient, user_repo: UserRepository):
        self.jwks = jwks_client
        self.users = user_repo

    async def resolve_user_from_token(self, bearer_token: str) -> User:
        claims = await self.jwks.decode_and_verify(bearer_token)
        user = from_claims(claims)
        await self.users.upsert(user)
        return user

    async def upsert_from_claims(self, claims: dict) -> User:
        user = from_claims(claims)
        await self.users.upsert(user)
        return user
