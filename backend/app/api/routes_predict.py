from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.rate_limit import rate_limiter
from app.core.response import success_response
from app.models.health_entry import HealthEntry
from app.models.user import User
from app.schemas.predict import PredictionInput
from app.services.nlp_service import symptom_extractor
from app.services.prediction_service import prediction_engine
from app.services.recommendation_service import recommendation_for
from app.services.risk_service import calculate_risk

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("")
def predict_condition(
    payload: PredictionInput,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rate_limiter.check(f"{current_user.id}:{request.client.host}")

    extracted = symptom_extractor.extract(payload.symptoms_text)
    payload_data = payload.model_dump()
    predictions = prediction_engine.predict_top3(payload_data, extracted.tags)
    top_conf = predictions[0]["confidence"] if predictions else 0.0

    risk = calculate_risk(payload_data, top_conf)
    top_features = prediction_engine.explain(payload_data, extracted.tags, predictions[0]["condition"])

    for row in predictions:
        row["recommended_next_steps"] = recommendation_for(row["condition"])

    response = {
        "symptom_tags": extracted.tags,
        "nlp_source": extracted.source,
        "predictions": predictions,
        "risk_score": risk.score,
        "risk_level": risk.level,
        "emergency_warning": risk.emergency_warning,
        "warning_message": risk.warning_message,
        "top_contributing_features": top_features,
        "disclaimer": "This is not medical advice. Consult a licensed clinician for diagnosis.",
    }

    if payload.save_entry:
        entry = HealthEntry(
            user_id=current_user.id,
            recorded_at=datetime.now(UTC),
            symptoms_text=payload.symptoms_text,
            symptom_tags=extracted.tags,
            heart_rate=payload.heart_rate,
            systolic_bp=payload.systolic_bp,
            diastolic_bp=payload.diastolic_bp,
            temperature=payload.temperature,
            spo2=payload.spo2,
            glucose=payload.glucose,
            weight=payload.weight,
            risk_score=risk.score,
            risk_level=risk.level,
            predictions=predictions,
            explanation=top_features,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        response["entry_id"] = entry.id

    return success_response(response, "Prediction completed")


@router.post("/extract-symptoms")
def extract_symptoms(payload: dict[str, str]):
    text = payload.get("symptoms_text", "")
    extracted = symptom_extractor.extract(text)
    return success_response({"symptom_tags": extracted.tags, "source": extracted.source})
