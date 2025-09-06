from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    code: str = Field(..., examples=["AUTH_INVALID_TOKEN"])
    message: str = Field(..., examples=["Invalid or expired token"])
    details: dict | None = None
