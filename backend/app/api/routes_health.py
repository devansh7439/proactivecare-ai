from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.response import success_response
from app.models.health_entry import HealthEntry
from app.models.user import User
from app.schemas.health import HealthEntryCreate, HealthEntryResponse, HealthEntryUpdate

router = APIRouter(prefix="/health-entries", tags=["Health Entries"])


@router.post("")
def create_entry(
    payload: HealthEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = HealthEntry(user_id=current_user.id, **payload.model_dump(exclude_unset=True))
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return success_response(HealthEntryResponse.model_validate(entry).model_dump(), "Entry created")


@router.get("")
def list_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = (
        db.execute(select(HealthEntry).where(HealthEntry.user_id == current_user.id).order_by(desc(HealthEntry.recorded_at)))
        .scalars()
        .all()
    )
    data = [HealthEntryResponse.model_validate(entry).model_dump() for entry in entries]
    return success_response(data)


@router.get("/{entry_id}")
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.execute(select(HealthEntry).where(HealthEntry.id == entry_id, HealthEntry.user_id == current_user.id))
        .scalar_one_or_none()
    )
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return success_response(HealthEntryResponse.model_validate(entry).model_dump())


@router.put("/{entry_id}")
def update_entry(
    entry_id: int,
    payload: HealthEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.execute(select(HealthEntry).where(HealthEntry.id == entry_id, HealthEntry.user_id == current_user.id))
        .scalar_one_or_none()
    )
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(entry, field, value)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return success_response(HealthEntryResponse.model_validate(entry).model_dump(), "Entry updated")


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.execute(select(HealthEntry).where(HealthEntry.id == entry_id, HealthEntry.user_id == current_user.id))
        .scalar_one_or_none()
    )
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return success_response(None, "Entry deleted")
