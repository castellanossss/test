from fastapi import APIRouter, Depends
from app.auth.api.deps import get_current_user
from app.auth.schemas.auth import AuthMeResponse
from app.auth.infra.mappers.user_mapper import to_dto

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/health", summary="Healthcheck", response_model=dict)
async def health():
    return {"ok": True}

@router.get("/me", summary="Identidad por JWT", response_model=AuthMeResponse)
async def me(user = Depends(get_current_user)):
    return {"user": to_dto(user)}
