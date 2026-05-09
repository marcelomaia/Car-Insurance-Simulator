# Running (Docker) — evaluator checklist

From the **repository root**:

```bash
docker compose up --build
```

When the API is up:

| | URL |
|--|-----|
| **Swagger** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health** | http://localhost:8000/health |

### Configuration (optional)

Copy the example file and edit tariff parameters as needed:

```bash
cp .env.example .env
```

You can change any **`CAR_INSURANCE_*`** value in **`.env`** (coverage factor, rate per year, rate per value chunk, chunk size — see comments inside [`.env.example`](.env.example)). Docker Compose loads **`.env`** from the repo root and injects those variables into the container. If **`.env`** does not exist, the app uses the built-in defaults.

---

## Smoke test after containers start

```bash
curl -s http://localhost:8000/health
```

Expected: `{"status":"ok"}`.

---

## Simulation (`POST /v1/premium/simulate`)

**Request** (matches [readme.md](readme.md) decade example — **10%** intrinsic rate when the car is **10** years old and **$100k**, **10%** deductible, **$50** broker fee):

```bash
curl -s -X POST http://localhost:8000/v1/premium/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "broker_fee": 50,
    "deductible_percentage": 0.1,
    "make": "Toyota",
    "model": "Corolla",
    "value": 100000,
    "year": 2016
  }'
```

**Expected JSON** if the container’s calendar year is **2026** and defaults apply (`CAR_INSURANCE_*` unchanged):

```json
{
  "applied_rate": 0.1,
  "calculated_premium": 9050,
  "deductible_value": 10000,
  "make": "Toyota",
  "model": "Corolla",
  "policy_limit": 90000,
  "value": 100000,
  "year": 2016
}
```

Vehicle age uses **`datetime.now().year`** inside the app; if the host year differs, **`applied_rate`** / **`calculated_premium`** change accordingly.

**Domain failure** (**422**): `{"detail":{"code":"…","message":"…"}}` — e.g. `invalid_deductible_percentage`, `negative_applied_rate`. Full contract: [readme.md](readme.md) § Interface / §5.
