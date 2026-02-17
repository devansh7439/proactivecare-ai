from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.response import success_response
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserProfileResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _issue_tokens(user_id: int, db: Session) -> TokenResponse:
    access, _ = create_access_token(str(user_id))
    refresh, jti, expires = create_refresh_token(str(user_id))
    db.add(RefreshToken(user_id=user_id, jti=jti, expires_at=expires, revoked=False))
    db.commit()
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in_seconds=60 * 30,
    )


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        age=payload.age,
        sex=payload.sex,
        height=payload.height,
        weight=payload.weight,
        known_conditions=payload.known_conditions or [],
        medications=payload.medications or [],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return success_response(UserProfileResponse.model_validate(user).model_dump(), "Registered successfully")


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_payload = _issue_tokens(user.id, db)
    return success_response(token_payload.model_dump(), "Login successful")


@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        token_data = decode_token(payload.refresh_token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    if token_data.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    jti = token_data.get("jti")
    user_id = int(token_data.get("sub"))
    token_record = db.execute(select(RefreshToken).where(RefreshToken.jti == jti)).scalar_one_or_none()
    if (
        not token_record
        or token_record.revoked
        or token_record.expires_at.replace(tzinfo=UTC) < datetime.now(UTC)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired or revoked")

    token_record.revoked = True
    db.commit()
    fresh_tokens = _issue_tokens(user_id, db)
    return success_response(fresh_tokens.model_dump(), "Token refreshed")


@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    try:
        token_data = decode_token(payload.refresh_token)
    except Exception:  # noqa: BLE001
        return success_response(None, "Logged out")

    jti = token_data.get("jti")
    if not jti:
        return success_response(None, "Logged out")

    token_record = db.execute(select(RefreshToken).where(RefreshToken.jti == jti)).scalar_one_or_none()
    if token_record:
        token_record.revoked = True
        db.commit()
    return success_response(None, "Logged out")
