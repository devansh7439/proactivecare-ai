from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskResult:
    score: int
    level: str
    emergency_warning: bool
    warning_message: str | None


def _add_for_range(value: float | None, low: float, high: float, mild: int, severe: int) -> int:
    if value is None:
        return 0
    if value < low or value > high:
        severe_band = (low - (low * 0.1), high + (high * 0.1))
        if value < severe_band[0] or value > severe_band[1]:
            return severe
        return mild
    return 0


def calculate_risk(vitals: dict, top_confidence: float) -> RiskResult:
    score = 0
    emergency = False
    warning = None

    score += _add_for_range(vitals.get("heart_rate"), 60, 100, 7, 15)
    score += _add_for_range(vitals.get("systolic_bp"), 90, 130, 8, 16)
    score += _add_for_range(vitals.get("diastolic_bp"), 60, 85, 8, 16)
    score += _add_for_range(vitals.get("temperature"), 36.1, 37.7, 10, 18)
    score += _add_for_range(vitals.get("spo2"), 95, 100, 12, 24)
    score += _add_for_range(vitals.get("glucose"), 70, 140, 8, 16)

    score += int(max(0, min(1, top_confidence)) * 25)
    score = max(0, min(100, score))

    if score >= 67:
        level = "High"
    elif score >= 34:
        level = "Moderate"
    else:
        level = "Low"

    hr = vitals.get("heart_rate")
    sbp = vitals.get("systolic_bp")
    dbp = vitals.get("diastolic_bp")
    temp = vitals.get("temperature")
    spo2 = vitals.get("spo2")
    glucose = vitals.get("glucose")

    dangerous = [
        spo2 is not None and spo2 < 90,
        hr is not None and (hr < 40 or hr > 150),
        sbp is not None and sbp > 180,
        dbp is not None and dbp > 120,
        temp is not None and temp >= 39.5,
        glucose is not None and (glucose < 54 or glucose > 300),
    ]
    if any(dangerous):
        emergency = True
        warning = "Dangerously abnormal vitals detected. Seek medical care now."
        score = max(score, 85)
        level = "High"

    return RiskResult(score=score, level=level, emergency_warning=emergency, warning_message=warning)
