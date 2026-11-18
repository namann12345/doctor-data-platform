# Doctor Data Platform

A credit-based healthcare professional discovery platform built for the **Multiplier AI Business Analyst Assessment**.

> **All doctor data is fictional. All payments are simulated. No real charges are made.**

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Seed the database (31 doctors, 2 demo users, 4 packages)
python seed_data.py

# Start the API server
uvicorn app.main:app --reload --port 8000
```

API docs available at **http://localhost:8000/docs**

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

App available at **http://localhost:5173**

---

## Demo Credentials

| Role | Email | Password | Credits |
|------|-------|----------|---------|
| Regular User | `user@demo.com` | `Demo@1234` | 150 |
| Admin | `admin@demo.com` | `Admin@1234` | 500 |

---

## Assessment Tasks

| Task | Description | Document |
|------|-------------|----------|
| 1. FRD | Functional Requirements (50 requirements, 5 modules) | [`docs/01_FRD.md`](docs/01_FRD.md) |
| 2. Business Rules | 15 rules + 5 scenarios (SC-001 to SC-005) | [`docs/02_Business_Rules_Scenarios.md`](docs/02_Business_Rules_Scenarios.md) |
| 3. Workflow Diagrams | 3 Mermaid flowcharts | [`docs/03_Workflow_Diagrams.md`](docs/03_Workflow_Diagrams.md) |
| 4. Wireframes | 4 screens (ASCII + annotations) | [`docs/04_Wireframes.md`](docs/04_Wireframes.md) |
| 5. Assumptions | 17 assumptions + 20 client questions | [`docs/05_Assumptions_Questions.md`](docs/05_Assumptions_Questions.md) |

**Primary submission:** [`docs/Assessment/Multiplier_AI_BA_Assessment.md`](docs/Assessment/Multiplier_AI_BA_Assessment.md)

---

## Business Scenarios Implemented

| ID | Scenario | How to Test |
|----|----------|-------------|
| SC-001 | Insufficient credits → unlock blocked | Register new user (0 credits) → try unlocking a doctor |
| SC-002 | Payment failure → no credits | Buy Credits → select any package → choose ❌ Failed mode |
| SC-003 | Payment pending → held until admin reconciles | Buy Credits → choose ⏳ Pending mode |
| SC-004 | No search results → empty state | Doctor Search → apply filters with zero matches |
| SC-005 | Duplicate payment → idempotent | Same `idempotency_key` sent twice returns original result |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI 0.111 · Python 3.10 · SQLAlchemy 2.0 · SQLite |
| Auth | JWT (python-jose) · bcrypt (passlib) |
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS |
| State | @tanstack/react-query · Context API |
| Charts | Recharts |
| Testing | Pytest · 34 auth integration tests |

---

## Project Structure

```
doctor data platform/
├── backend/
│   ├── app/
│   │   ├── api/            # 7 route modules (auth, doctors, credits, etc.)
│   │   ├── models/         # 7 SQLAlchemy models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── repositories/   # Database access layer
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Security helpers (JWT, bcrypt)
│   │   ├── config.py       # Settings
│   │   ├── database.py     # Engine + session
│   │   ├── dependencies.py # Auth dependencies
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Pytest tests
│   ├── seed_data.py        # Demo data seeder
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # UI components (layout, dashboard, ui)
│   │   ├── contexts/       # Auth + Toast context
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # API client + constants
│   │   ├── pages/          # 9 page components
│   │   ├── services/       # API service functions
│   │   ├── types/          # TypeScript type definitions
│   │   ├── App.tsx         # Router
│   │   └── main.tsx        # Entry point
│   ├── package.json
│   └── vite.config.ts      # Dev proxy → localhost:8000
├── docs/
│   ├── 01_FRD.md
│   ├── 02_Business_Rules_Scenarios.md
│   ├── 03_Workflow_Diagrams.md
│   ├── 04_Wireframes.md
│   ├── 05_Assumptions_Questions.md
│   ├── 06_API_Documentation.md
│   ├── 07_Database_Design.md
│   ├── 08_Test_Cases.md
│   └── Assessment/
│       └── Multiplier_AI_BA_Assessment.md
├── .gitignore
└── README.md
```

---

## Running Tests

```bash
cd backend

# Auth integration tests (34 assertions)
python tests/test_auth_integration.py
```

---

## License

Assessment submission — Multiplier AI Limited.
