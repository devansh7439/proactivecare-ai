from __future__ import annotations

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    symptoms_text: str = Field(min_length=3, max_length=5000)
    heart_rate: int | None = Field(default=None, ge=20, le=250)
    systolic_bp: int | None = Field(default=None, ge=40, le=300)
    diastolic_bp: int | None = Field(default=None, ge=30, le=200)
    temperature: float | None = Field(default=None, ge=30, le=45)
    spo2: float | None = Field(default=None, ge=40, le=100)
    glucose: float | None = Field(default=None, ge=20, le=600)
    weight: float | None = Field(default=None, ge=1, le=500)
    save_entry: bool = True


class ConditionPrediction(BaseModel):
    condition: str
    confidence: float
    recommended_next_steps: list[str]


class PredictionResponse(BaseModel):
    symptom_tags: list[str]
    predictions: list[ConditionPrediction]
    risk_score: int
    risk_level: str
    emergency_warning: bool
    warning_message: str | None = None
    top_contributing_features: list[str]
    disclaimer: str
