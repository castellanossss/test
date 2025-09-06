from fastapi import APIRouter, Request

router = APIRouter(prefix="/auth/webhooks", tags=["auth-webhooks"])

@router.post("/clerk", summary="Webhook Clerk (stub)", status_code=202)
async def clerk_webhook(req: Request):
    _ = await req.body()  # TODO: verificar firma y despachar eventos
    return {"accepted": True}
