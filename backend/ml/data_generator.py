from __future__ import annotations

import random

import pandas as pd

CONDITIONS = [
    "Common Cold",
    "Influenza",
    "Hypertension",
    "Type 2 Diabetes",
    "Pneumonia",
    "COVID-19",
    "Migraine",
]

SYMPTOM_POOL = {
    "Common Cold": ["cough", "sore throat", "runny nose", "mild headache"],
    "Influenza": ["fever", "fatigue", "body ache", "cough"],
    "Hypertension": ["headache", "dizziness", "chest pressure"],
    "Type 2 Diabetes": ["fatigue", "frequent urination", "thirst", "blurred vision"],
    "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain"],
    "COVID-19": ["fever", "cough", "fatigue", "shortness of breath"],
    "Migraine": ["headache", "nausea", "light sensitivity"],
}


def _sample_vitals(condition: str) -> dict:
    base = {
        "heart_rate": random.randint(60, 95),
        "systolic_bp": random.randint(100, 130),
        "diastolic_bp": random.randint(65, 85),
        "temperature": round(random.uniform(36.2, 37.3), 1),
        "spo2": round(random.uniform(95, 99), 1),
        "glucose": round(random.uniform(80, 130), 1),
        "weight": round(random.uniform(50, 90), 1),
    }

    if condition in {"Influenza", "Pneumonia", "COVID-19"}:
        base["temperature"] = round(random.uniform(37.8, 40.0), 1)
        base["heart_rate"] = random.randint(85, 130)
    if condition in {"Pneumonia", "COVID-19"}:
        base["spo2"] = round(random.uniform(86, 95), 1)
    if condition == "Hypertension":
        base["systolic_bp"] = random.randint(140, 190)
        base["diastolic_bp"] = random.randint(90, 125)
    if condition == "Type 2 Diabetes":
        base["glucose"] = round(random.uniform(150, 320), 1)
    if condition == "Migraine":
        base["heart_rate"] = random.randint(65, 110)
    return base


def generate_synthetic_dataset(n_samples: int = 3000, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    rows = []
    for _ in range(n_samples):
        condition = random.choice(CONDITIONS)
        symptoms = random.sample(SYMPTOM_POOL[condition], k=min(3, len(SYMPTOM_POOL[condition])))
        symptom_text = ", ".join(symptoms)
        vitals = _sample_vitals(condition)
        rows.append(
            {
                "symptoms_text": symptom_text,
                "heart_rate": vitals["heart_rate"],
                "systolic_bp": vitals["systolic_bp"],
                "diastolic_bp": vitals["diastolic_bp"],
                "temperature": vitals["temperature"],
                "spo2": vitals["spo2"],
                "glucose": vitals["glucose"],
                "weight": vitals["weight"],
                "condition": condition,
            }
        )
    return pd.DataFrame(rows)
