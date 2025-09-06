import os

CLERK_ISSUER = os.getenv("CLERK_ISSUER", "").rstrip("/")
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL") or (f"{CLERK_ISSUER}/.well-known/jwks.json" if CLERK_ISSUER else "")
CLERK_AUDIENCE = os.getenv("CLERK_AUDIENCE")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/ehc_auth")