from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.response import success_response
from app.models.user import User
from app.schemas.auth import UserProfileResponse
from app.schemas.profile import ProfileUpdateRequest

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return success_response(UserProfileResponse.model_validate(current_user).model_dump())


@router.put("/me")
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(current_user, field, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return success_response(UserProfileResponse.model_validate(current_user).model_dump(), "Profile updated")
