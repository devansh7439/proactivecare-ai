from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict | list | str | None = None
    errors: dict | list | str | None = None
