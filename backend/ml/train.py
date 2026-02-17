from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

from ml.data_generator import generate_synthetic_dataset

NUMERIC_FEATURES = [
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "temperature",
    "spo2",
    "glucose",
    "weight",
]


def train_and_save(output_dir: Path | str = "ml/artifacts") -> dict:
    backend_root = Path(__file__).resolve().parents[1]
    output = Path(output_dir)
    if not output.is_absolute():
        output = backend_root / output
    output.mkdir(parents=True, exist_ok=True)

    data = generate_synthetic_dataset(n_samples=3500, seed=42)
    x = data[["symptoms_text", *NUMERIC_FEATURES]]
    y = data["condition"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(ngram_range=(1, 2), max_features=500), "symptoms_text"),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocess),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=250,
                    random_state=42,
                    class_weight="balanced_subsample",
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    joblib.dump(model, output / "model.pkl")
    text_vectorizer = model.named_steps["preprocess"].named_transformers_["text"]
    joblib.dump(text_vectorizer, output / "vectorizer.pkl")

    metadata = {
        "classes": sorted(list(set(y))),
        "samples": len(data),
        "metrics_macro_f1": report["macro avg"]["f1-score"],
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


if __name__ == "__main__":
    info = train_and_save()
    print("Training complete:", info)
