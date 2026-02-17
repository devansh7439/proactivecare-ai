from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.health_entry import HealthEntry
from app.models.user import User


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "demo@proactivecare.ai").first()
        if not user:
            user = User(
                email="demo@proactivecare.ai",
                hashed_password=hash_password("DemoPass123"),
                age=34,
                sex="female",
                height=165.0,
                weight=64.0,
                known_conditions=["mild_asthma"],
                medications=["albuterol"],
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        for i in range(6):
            entry = HealthEntry(
                user_id=user.id,
                recorded_at=datetime.now(UTC) - timedelta(days=6 - i),
                symptoms_text="mild cough and fatigue",
                symptom_tags=["cough", "fatigue"],
                heart_rate=78 + i,
                systolic_bp=118 + i,
                diastolic_bp=76 + i,
                temperature=36.8 + (i * 0.05),
                spo2=98 - (i * 0.2),
                glucose=102 + i,
                weight=64 + (i * 0.1),
                risk_score=20 + i * 3,
                risk_level="Low" if i < 4 else "Moderate",
                predictions=[{"condition": "Common Cold", "confidence": 0.61}],
                explanation=["cough", "fatigue"],
            )
            db.add(entry)
        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
