from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import BaseSchema


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    age: int | None = Field(default=None, ge=0, le=130)
    sex: Literal["male", "female", "other"] | None = None
    height: float | None = Field(default=None, ge=30, le=260)
    weight: float | None = Field(default=None, ge=1, le=500)
    known_conditions: list[str] | None = None
    medications: list[str] | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class UserProfileResponse(BaseSchema):
    id: int
    email: EmailStr
    age: int | None = None
    sex: str | None = None
    height: float | None = None
    weight: float | None = None
    known_conditions: list[str] | None = None
    medications: list[str] | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
