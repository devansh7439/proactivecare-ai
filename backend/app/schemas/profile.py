from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.auth import UserProfileResponse


class ProfileUpdateRequest(BaseModel):
    age: int | None = Field(default=None, ge=0, le=130)
    sex: Literal["male", "female", "other"] | None = None
    height: float | None = Field(default=None, ge=30, le=260)
    weight: float | None = Field(default=None, ge=1, le=500)
    known_conditions: list[str] | None = None
    medications: list[str] | None = None


ProfileResponse = UserProfileResponse
