from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from app.core.config import settings

logger = logging.getLogger(__name__)


class PredictionEngine:
    def __init__(self) -> None:
        self.model = None
        self.vectorizer = None
        self._ensure_artifacts()
        self._load_artifacts()

    def _ensure_artifacts(self) -> None:
        model_path = settings.model_path
        vectorizer_path = settings.vectorizer_path
        if model_path.exists() and vectorizer_path.exists():
            return
        logger.info("Model artifacts missing. Training synthetic baseline model.")
        from ml.train import train_and_save

        train_and_save(Path(settings.model_dir))

    def _load_artifacts(self) -> None:
        self.model = joblib.load(settings.model_path)
        self.vectorizer = joblib.load(settings.vectorizer_path)

    def _build_dataframe(self, payload: dict[str, Any], symptom_tags: list[str]) -> pd.DataFrame:
        text = payload["symptoms_text"]
        if symptom_tags:
            text = f"{text}. symptoms: {', '.join(symptom_tags)}"

        return pd.DataFrame(
            [
                {
                    "symptoms_text": text,
                    "heart_rate": payload.get("heart_rate") or 0,
                    "systolic_bp": payload.get("systolic_bp") or 0,
                    "diastolic_bp": payload.get("diastolic_bp") or 0,
                    "temperature": payload.get("temperature") or 0.0,
                    "spo2": payload.get("spo2") or 0.0,
                    "glucose": payload.get("glucose") or 0.0,
                    "weight": payload.get("weight") or 0.0,
                }
            ]
        )

    def predict_top3(self, payload: dict[str, Any], symptom_tags: list[str]) -> list[dict]:
        frame = self._build_dataframe(payload, symptom_tags)
        probs = self.model.predict_proba(frame)[0]
        classes = self.model.classes_
        top_indices = np.argsort(probs)[::-1][:3]
        return [
            {"condition": str(classes[idx]), "confidence": round(float(probs[idx]), 4)}
            for idx in top_indices
        ]

    def explain(self, payload: dict[str, Any], symptom_tags: list[str], top_condition: str) -> list[str]:
        frame = self._build_dataframe(payload, symptom_tags)
        try:
            import shap

            preprocess = self.model.named_steps["preprocess"]
            classifier = self.model.named_steps["clf"]
            transformed = preprocess.transform(frame)
            transformed_dense = transformed.toarray() if hasattr(transformed, "toarray") else transformed
            feature_names = preprocess.get_feature_names_out()

            explainer = shap.TreeExplainer(classifier)
            shap_values = explainer.shap_values(transformed_dense)
            class_index = int(np.where(classifier.classes_ == top_condition)[0][0])
            class_values = shap_values[class_index][0]

            top_features = np.argsort(np.abs(class_values))[::-1][:5]
            output = []
            for idx in top_features:
                name = str(feature_names[idx]).replace("text__", "").replace("num__", "")
                output.append(name.replace("_", " "))
            return output
        except Exception as exc:  # noqa: BLE001
            logger.warning("SHAP explanation failed, using fallback: %s", exc)
            return self._fallback_explain(payload, symptom_tags)

    def _fallback_explain(self, payload: dict[str, Any], symptom_tags: list[str]) -> list[str]:
        features: list[str] = []
        temp = payload.get("temperature")
        spo2 = payload.get("spo2")
        hr = payload.get("heart_rate")
        sbp = payload.get("systolic_bp")
        glucose = payload.get("glucose")

        if temp and temp > 37.8:
            features.append("elevated temperature")
        if spo2 and spo2 < 95:
            features.append("low SpO2")
        if hr and (hr < 60 or hr > 100):
            features.append("abnormal heart rate")
        if sbp and sbp > 140:
            features.append("high systolic blood pressure")
        if glucose and glucose > 180:
            features.append("high glucose")
        for tag in symptom_tags[:3]:
            features.append(tag.replace("_", " "))
        return features[:5] if features else ["reported symptom pattern"]


prediction_engine = PredictionEngine()
