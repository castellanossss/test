from app.auth.domain.models import User
from app.auth.schemas.user import UserDTO

def to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        sede_id=user.sede_id,
    )

def from_claims(claims: dict) -> User:
    email = (
        claims.get("email") or
        claims.get("primary_email") or
        None
    )

    given = (claims.get("given_name") or claims.get("first_name") or "").strip()
    family = (claims.get("family_name") or claims.get("last_name") or "").strip()
    name = claims.get("name")
    if not name:
        name = " ".join([p for p in (given, family) if p]) or None

    role = (claims.get("role") or "client")

    return User(
        id=claims["sub"],
        email=email,
        full_name=name,
        role=role,
        sede_id=claims.get("sede_id"),
    )
