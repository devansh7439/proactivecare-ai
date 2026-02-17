from __future__ import annotations

CONDITION_RECOMMENDATIONS: dict[str, list[str]] = {
    "Common Cold": ["Rest and hydrate", "Use steam inhalation", "Monitor fever and symptoms"],
    "Influenza": ["Rest and fluids", "Consider antiviral consultation if early", "Monitor breathing and fever"],
    "Hypertension": ["Reduce sodium intake", "Track blood pressure daily", "Consult physician for medication review"],
    "Type 2 Diabetes": ["Monitor glucose regularly", "Follow a low-glycemic diet", "Schedule follow-up with clinician"],
    "Pneumonia": ["Seek urgent clinical evaluation", "Monitor oxygen saturation", "Avoid strenuous activity"],
    "COVID-19": ["Isolate if symptomatic", "Track oxygen and fever", "Seek care for breathing difficulty"],
    "Migraine": ["Hydrate and rest in dark room", "Avoid trigger foods", "Consult doctor for persistent episodes"],
}


def recommendation_for(condition: str) -> list[str]:
    return CONDITION_RECOMMENDATIONS.get(
        condition,
        ["Track symptoms closely", "Maintain hydration and rest", "Consult a healthcare professional if symptoms worsen"],
    )
