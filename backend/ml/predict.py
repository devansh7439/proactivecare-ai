from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd


def run_prediction(model_path: Path, symptoms_text: str) -> None:
    model = joblib.load(model_path)
    sample = pd.DataFrame(
        [
            {
                "symptoms_text": symptoms_text,
                "heart_rate": 90,
                "systolic_bp": 120,
                "diastolic_bp": 80,
                "temperature": 37.8,
                "spo2": 96.0,
                "glucose": 110.0,
                "weight": 70.0,
            }
        ]
    )
    probs = model.predict_proba(sample)[0]
    classes = model.classes_
    top = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
    for label, score in top:
        print(f"{label}: {score:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="ml/artifacts/model.pkl")
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    backend_root = Path(__file__).resolve().parents[1]
    model = Path(args.model)
    if not model.is_absolute():
        model = backend_root / model
    run_prediction(model, args.text)
