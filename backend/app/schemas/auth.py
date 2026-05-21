from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6)
    role: str = Field("analyst", pattern="^(analyst|admin|viewer)$")


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    username: str
    password: str
