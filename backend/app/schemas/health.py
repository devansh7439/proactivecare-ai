from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema


class HealthEntryBase(BaseModel):
    recorded_at: datetime | None = None
    symptoms_text: str = Field(min_length=3, max_length=5000)
    symptom_tags: list[str] = Field(default_factory=list)
    heart_rate: int | None = Field(default=None, ge=20, le=250)
    systolic_bp: int | None = Field(default=None, ge=40, le=300)
    diastolic_bp: int | None = Field(default=None, ge=30, le=200)
    temperature: float | None = Field(default=None, ge=30, le=45)
    spo2: float | None = Field(default=None, ge=40, le=100)
    glucose: float | None = Field(default=None, ge=20, le=600)
    weight: float | None = Field(default=None, ge=1, le=500)


class HealthEntryCreate(HealthEntryBase):
    risk_score: float | None = Field(default=None, ge=0, le=100)
    risk_level: str | None = None
    predictions: list[dict] | None = None
    explanation: list[str] | None = None


class HealthEntryUpdate(BaseModel):
    symptoms_text: str | None = Field(default=None, min_length=3, max_length=5000)
    symptom_tags: list[str] | None = None
    heart_rate: int | None = Field(default=None, ge=20, le=250)
    systolic_bp: int | None = Field(default=None, ge=40, le=300)
    diastolic_bp: int | None = Field(default=None, ge=30, le=200)
    temperature: float | None = Field(default=None, ge=30, le=45)
    spo2: float | None = Field(default=None, ge=40, le=100)
    glucose: float | None = Field(default=None, ge=20, le=600)
    weight: float | None = Field(default=None, ge=1, le=500)


class HealthEntryResponse(BaseSchema):
    id: int
    user_id: int
    recorded_at: datetime
    symptoms_text: str
    symptom_tags: list[str]
    heart_rate: int | None = None
    systolic_bp: int | None = None
    diastolic_bp: int | None = None
    temperature: float | None = None
    spo2: float | None = None
    glucose: float | None = None
    weight: float | None = None
    risk_score: float | None = None
    risk_level: str | None = None
    predictions: list[dict] | None = None
    explanation: list[str] | None = None
