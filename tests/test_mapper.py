from app.auth.infra.mappers.user_mapper import from_claims, to_dto
from app.auth.domain.models import User

def test_from_claims_fullname_from_given_family():
    claims = {
        "sub": "user_123",
        "email": "foo@example.com",
        "given_name": "Ada",
        "family_name": "Lovelace",
    }
    u = from_claims(claims)
    assert u.id == "user_123"
    assert u.email == "foo@example.com"
    assert u.full_name == "Ada Lovelace"
    assert u.role == "client"

def test_from_claims_fullname_from_name():
    claims = {
        "sub": "user_456",
        "email": "bar@example.com",
        "name": "Grace Hopper",
    }
    u = from_claims(claims)
    assert u.full_name == "Grace Hopper"

def test_to_dto_roundtrip():
    u = User(id="u1", email="a@b.com", full_name="Test User", role="client", sede_id=None)
    dto = to_dto(u)
    assert dto.id == "u1"
    assert dto.email == "a@b.com"
    assert dto.full_name == "Test User"
    assert dto.role == "client"
