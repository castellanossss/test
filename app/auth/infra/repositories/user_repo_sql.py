from sqlalchemy import select
from app.auth.domain.interfaces import UserRepository
from app.auth.domain.models import User
from app.auth.infra.repositories.models import UserRecord
from app.auth.infra.db.session import SessionLocal

def to_domain(rec: UserRecord) -> User:
    return User(
        id=rec.id,
        email=rec.email,
        full_name=rec.full_name,
        role=rec.role,
        sede_id=rec.sede_id,
    )

class SqlUserRepo(UserRepository):
    async def get(self, user_id: str) -> User | None:
        async with SessionLocal() as s:
            res = await s.execute(select(UserRecord).where(UserRecord.id == user_id))
            rec = res.scalar_one_or_none()
            return to_domain(rec) if rec else None

    async def upsert(self, user: User) -> User:
        async with SessionLocal() as s:
            rec = await s.get(UserRecord, user.id)

            if rec is None:
                rec = UserRecord(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    role=(user.role or "client"),
                    sede_id=user.sede_id,
                )
                s.add(rec)
            else:
                if user.email:
                    rec.email = user.email
                if user.full_name:
                    rec.full_name = user.full_name

                if user.role:
                    incoming = user.role
                    current = (rec.role or "client")
                    if incoming != current:
                        if incoming != "client" or current in (None, "", "client"):
                            rec.role = incoming

                if user.sede_id is not None:
                    rec.sede_id = user.sede_id

            await s.commit()
            await s.refresh(rec)
            return to_domain(rec)
