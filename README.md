# ProactiveCare AI

ProactiveCare AI is a full-stack MVP for proactive health monitoring and AI-assisted condition risk assessment.

It includes:
- JWT auth (access + refresh tokens)
- User profile management
- Health entry CRUD (vitals + symptoms free text)
- NLP symptom extraction (DistilBERT if GPU available, TF-IDF + deterministic keyword fallback otherwise)
- Top-3 condition prediction with confidence scores
- Explainability panel (SHAP preferred, fallback heuristic)
- Risk scoring (0-100) with emergency warning for dangerously abnormal vitals
- History trends dashboard with charts

> Disclaimer: This app is not medical advice. Always consult licensed clinicians for diagnosis or treatment.

## Architecture

- Frontend: React + TypeScript + Vite + Tailwind + Recharts
- Backend: FastAPI + SQLAlchemy + Alembic + JWT
- ML: Scikit-learn RandomForest baseline + TF-IDF text features + optional DistilBERT symptom extraction
- Database: PostgreSQL in Docker, SQLite fallback for local tests/dev

## Project Structure

```text
proactivecare-ai/
  backend/
    alembic/
    app/
    ml/
    scripts/
    tests/
    Dockerfile
    requirements.txt
  frontend/
    src/
    Dockerfile
  docs/
    curl_examples.md
    proactivecare_postman_collection.json
  docker-compose.yml
  .env.example
  README.md
```

## Environment Variables

Copy `.env.example` at project root:

```bash
cp .env.example .env
```

Backend env reference: `backend/.env.example`  
Frontend env reference: `frontend/.env.example`

## Run with Docker

```bash
docker compose up --build
```

Services:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Local Run (without Docker)

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m ml.train
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Model Training

Synthetic data pipeline is isolated in `backend/ml`.

Train/retrain artifacts:
```bash
cd backend
python -m ml.train
```

Generated artifacts:
- `backend/ml/artifacts/model.pkl`
- `backend/ml/artifacts/vectorizer.pkl`

## Seed Sample Data

```bash
cd backend
python -m scripts.seed_data
```

Demo user created:
- Email: `demo@proactivecare.ai`
- Password: `DemoPass123`

## Tests

```bash
cd backend
pytest -q
```

## Lint/Format

```bash
cd backend
black .
isort .
ruff check .
```

## API Examples

- Curl: `docs/curl_examples.md`
- Postman: `docs/proactivecare_postman_collection.json`
