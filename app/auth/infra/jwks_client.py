import time
import httpx
from jose import jwt
from app.auth.domain.interfaces import JWKSClient
from app.core.config import CLERK_JWKS_URL, CLERK_AUDIENCE, CLERK_ISSUER

class HTTPJWKSClient(JWKSClient):
    def __init__(self, jwks_url: str = CLERK_JWKS_URL, cache_ttl: int = 3600):
        if not jwks_url:
            raise RuntimeError("CLERK_JWKS_URL o CLERK_ISSUER no configurados")
        self.jwks_url = jwks_url
        self.cache_ttl = cache_ttl
        self._cache = None
        self._exp = 0

    async def get_signing_keys(self) -> dict:
        now = time.time()
        if not self._cache or self._exp < now:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(self.jwks_url)
                r.raise_for_status()
                self._cache = r.json()
                self._exp = now + self.cache_ttl
        return self._cache

    async def decode_and_verify(self, token: str, audience: str | None = CLERK_AUDIENCE, issuer: str | None = CLERK_ISSUER) -> dict:
        unverified = jwt.get_unverified_header(token)
        kid = unverified.get("kid")
        jwks = await self.get_signing_keys()
        key = next((k for k in jwks["keys"] if k.get("kid") == kid), None)
        if not key:
            raise ValueError("Signing key not found (kid mismatch)")

        options = {}
        if not audience:
            options["verify_aud"] = False
        if not issuer:
            options["verify_iss"] = False

        return jwt.decode(
            token,
            key,  # python-jose acepta JWK dict
            algorithms=[key.get("alg", "RS256")],
            audience=(audience or None),
            issuer=(issuer or None),
            options=options
        )
