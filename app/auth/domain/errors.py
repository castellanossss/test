from dataclasses import dataclass

@dataclass(frozen=True)
class DomainError(Exception):
    code: str
    message: str
    details: dict | None = None

AUTH_INVALID_TOKEN = DomainError(
    code="AUTH_INVALID_TOKEN",
    message="Invalid or expired token",
)

AUTH_FORBIDDEN = DomainError(
    code="AUTH_FORBIDDEN",
    message="Insufficient permissions",
)

AUTH_JWKS_ERROR = DomainError(
    code="AUTH_JWKS_ERROR",
    message="Unable to retrieve/parse JWKS",
)

USER_NOT_FOUND = DomainError(
    code="USER_NOT_FOUND",
    message="User not found",
)
