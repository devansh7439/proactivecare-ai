# Curl Examples

## Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123","age":30,"sex":"female"}'
```

## Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}'
```

## Predict + Save Entry
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{
    "symptoms_text":"fever, cough, shortness of breath",
    "heart_rate":118,
    "systolic_bp":145,
    "diastolic_bp":92,
    "temperature":39.1,
    "spo2":90,
    "glucose":130,
    "weight":72,
    "save_entry":true
  }'
```

## List History
```bash
curl -X GET http://localhost:8000/api/v1/health-entries \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
