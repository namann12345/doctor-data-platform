# Multiplier AI — Business Analyst Assessment Submission
## Doctor Data Platform

---

**Candidate:** Business Analyst Assessment Submission  
**Organisation:** Multiplier AI Limited  
**Assessment Type:** End-to-End Healthcare Data Platform BA & Development  
**Date:** November 2026  
**Version:** 1.0 — Final Submission  

---

> **Platform Inspiration:** Apollo 247 · Lucia Health · Practo  
> **Stack:** FastAPI (Python) · React (TypeScript) · SQLite · Tailwind CSS · JWT Auth  
> **Demo:** `user@demo.com / Demo@1234` | `admin@demo.com / Admin@1234`  
> **All doctor data is fictional. All payments are simulated (no real charges).**

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview & Architecture](#2-project-overview--architecture)
3. [Task 1 — Functional Requirements Document](#3-task-1--functional-requirements-document)
4. [Task 2 — Business Rules & Scenarios](#4-task-2--business-rules--scenarios)
5. [Task 3 — Workflow Diagrams](#5-task-3--workflow-diagrams)
6. [Task 4 — Wireframes](#6-task-4--wireframes)
7. [Task 5 — Assumptions & Client Questions](#7-task-5--assumptions--client-questions)
8. [Implementation Evidence](#8-implementation-evidence)
9. [How to Run the Application](#9-how-to-run-the-application)
10. [Conclusion](#10-conclusion)

---

## 1. Executive Summary

This submission presents a **complete, end-to-end Doctor Data Platform** built for the Multiplier AI Business Analyst assessment. The platform enables users to discover and access detailed healthcare professional profiles using a **credit-based access model** — inspired by platforms like Apollo 247, Lucia Health, and Practo.

### What Was Delivered

| Deliverable | Status | Detail |
|-------------|--------|--------|
| Task 1 — FRD | ✅ Complete | 5 modules, 36KB detailed document |
| Task 2 — Business Rules & Scenarios | ✅ Complete | 15 rules, 5 scenarios (SC-001 to SC-005) |
| Task 3 — Workflow Diagrams | ✅ Complete | 3 Mermaid flowcharts |
| Task 4 — Wireframes | ✅ Complete | 4 screens with ASCII + annotations |
| Task 5 — Assumptions & Questions | ✅ Complete | 17 assumptions, 20 questions, risk register |
| Backend API | ✅ Complete | 7 router modules, 23 tests, seed data |
| Frontend Web App | ✅ Complete | 9 pages, React/TypeScript, TypeScript compiles cleanly |
| Database | ✅ Complete | 7 tables, 31 doctors seeded, 2 demo users |
| Documentation | ✅ Complete | 7 doc files + this submission |

### Business Scenarios Implemented

All 5 required scenarios are implemented in the backend and demonstrated in the UI:

| Scenario | Description | Implementation |
|----------|-------------|----------------|
| SC-001 | Insufficient credits → unlock blocked | HTTP 402, inline error with Buy Credits CTA |
| SC-002 | Payment failure → no credits added | `payment_mode: "fail"`, status=failed, 0 credits |
| SC-003 | Payment pending → credits held | `payment_mode: "pending"`, admin reconcile endpoint |
| SC-004 | No search results → empty state | 200 OK with empty array, friendly UI guidance |
| SC-005 | Duplicate payment → idempotency | `idempotency_key` deduplication, original result returned |

---

## 2. Project Overview & Architecture

### Business Model

The Doctor Data Platform operates on a **credit-based access model**:

```
User Registers → Purchases Credits → Searches Doctors → Unlocks Profile (10 cr) → Views Contact Info
```

This model ensures:
- **Revenue generation** through credit packages
- **Quality gate** — users invest intentionally in profiles they want
- **Scalable pricing** — package tiers from ₹99 to ₹1,499
- **Auditability** — every credit movement is logged in the ledger

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND                             │
│  React + TypeScript + Vite + Tailwind CSS               │
│  Port: 5173                                             │
│  State: React Query + Context API                        │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP / JSON (JWT Bearer)
┌────────────────────────▼────────────────────────────────┐
│                     BACKEND                              │
│  FastAPI (Python 3.10) + Uvicorn                        │
│  Port: 8000                                             │
│  Auth: JWT (python-jose) + bcrypt                        │
│  Docs: /docs (Swagger UI)                               │
└────────────────────────┬────────────────────────────────┘
                         │ SQLAlchemy ORM
┌────────────────────────▼────────────────────────────────┐
│                    DATABASE                              │
│  SQLite (dev) → PostgreSQL (production)                  │
│  7 Tables: users, doctors, credit_packages,              │
│  payments, transactions, credit_ledger, doctor_unlocks   │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| Backend | FastAPI 0.111 | Async-ready, auto-docs, type-safe |
| Auth | JWT + bcrypt | Industry standard, stateless |
| ORM | SQLAlchemy 2.0 | Mature, schema migrations ready |
| Database | SQLite (dev) | Zero-config for assessment |
| Frontend | React 18 + TypeScript | Component-based, type safety |
| Build | Vite | Fast HMR, optimized builds |
| Styling | Tailwind CSS | Utility-first, responsive |
| State | @tanstack/react-query | Server state caching |
| Charts | Recharts | Credit balance visualization |
| Testing | Pytest + FastAPI TestClient | 23 test cases |

### Database Schema

```
users (id, email, full_name, hashed_password, credit_balance, is_admin, is_active)
  │
  ├── payments (id, user_id, credit_package_id, amount, status, idempotency_key, ...)
  ├── transactions (id, user_id, type, credits_delta, balance_after, description, ...)
  ├── credit_ledger (id, user_id, entry_type, credits, balance_before, balance_after, ...)
  └── doctor_unlocks (id, user_id, doctor_id, credits_spent, unlocked_at)

doctors (id, name, specialty, qualification, experience_years, hospital, city, 
         state, phone, email, consultation_fee, rating, total_reviews, bio)

credit_packages (id, name, credits, bonus_credits, price, is_featured, is_active)
```

---

## 3. Task 1 — Functional Requirements Document

> Full FRD: [`docs/01_FRD.md`](../01_FRD.md)

### Module Summary

#### M-001: User Authentication & Account Management (FR-001 to FR-010)

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-001 | User can self-register with name, email, password | Must Have |
| FR-002 | Passwords must be validated (8+ chars, uppercase, digit, special) | Must Have |
| FR-003 | Registered users can log in with email + password | Must Have |
| FR-004 | System issues JWT access tokens (24hr expiry) | Must Have |
| FR-005 | Users can view and edit their profile (name, email, phone) | Should Have |
| FR-006 | Users can change their password from profile settings | Should Have |
| FR-007 | Users can view current credit balance on every screen | Must Have |
| FR-008 | Duplicate email registration returns 400 error | Must Have |
| FR-009 | Invalid credentials return 401 Unauthorized | Must Have |
| FR-010 | Protected routes redirect unauthenticated users to login | Must Have |

#### M-002: Credit Purchase System (FR-011 to FR-020)

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-011 | Platform offers 4 credit packages (Starter/Growth/Professional/Enterprise) | Must Have |
| FR-012 | Each package shows: price, base credits, bonus credits, total credits | Must Have |
| FR-013 | User can select a package and proceed to payment | Must Have |
| FR-014 | Payment is simulated with 3 modes: success/fail/pending | Must Have |
| FR-015 | Successful payment adds credits + bonus to user balance | Must Have |
| FR-016 | Failed payment adds 0 credits; records failed status | Must Have |
| FR-017 | Pending payment holds credits until admin reconciliation | Must Have |
| FR-018 | Idempotency key prevents duplicate credit additions | Must Have |
| FR-019 | Each payment creates an entry in credit_packages and transactions | Must Have |
| FR-020 | User is shown purchase confirmation modal before payment | Should Have |

#### M-003: Doctor Search & Discovery (FR-021 to FR-030)

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-021 | Users can search doctors by name/keyword | Must Have |
| FR-022 | Filters: specialty, city, state, min experience, max consultation fee | Must Have |
| FR-023 | Doctor cards show: name, specialty, hospital, city, rating, experience | Must Have |
| FR-024 | Contact info (phone, email) is hidden until profile is unlocked | Must Have |
| FR-025 | Search results paginate (12 per page) | Should Have |
| FR-026 | Empty search results show friendly empty state with suggestions | Must Have |
| FR-027 | Filters can be cleared with a single "Clear All" action | Should Have |
| FR-028 | Result count is displayed with active filters indicated | Should Have |
| FR-029 | Doctors are sorted by rating (highest first) by default | Could Have |
| FR-030 | Search is debounced to avoid excess API calls | Should Have |

#### M-004: Profile Unlock System (FR-031 to FR-040)

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-031 | Unlocking a doctor profile costs exactly 10 credits | Must Have |
| FR-032 | User with insufficient credits sees 402 error and Buy Credits CTA | Must Have |
| FR-033 | Unlock is idempotent — re-viewing an unlocked profile costs 0 credits | Must Have |
| FR-034 | Unlock deducts 10 credits from user balance atomically | Must Have |
| FR-035 | Unlock creates a DoctorUnlock record and CreditLedger entry | Must Have |
| FR-036 | Unlocked profile reveals: phone, email, full bio, consultation fee | Must Have |
| FR-037 | User is shown confirmation prompt before deducting credits | Should Have |
| FR-038 | Dashboard shows count of doctors unlocked | Should Have |
| FR-039 | Unlock history visible in transaction log | Should Have |
| FR-040 | Unlocked doctor profiles are accessible from user's history | Could Have |

#### M-005: Transaction History & Dashboard (FR-041 to FR-050)

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-041 | Dashboard shows: credit balance, credits purchased, credits spent, doctors unlocked | Must Have |
| FR-042 | Credit balance history chart (line chart by date) | Should Have |
| FR-043 | Recent activity list (last 10 transactions) | Must Have |
| FR-044 | Full transaction log with pagination (credit purchases + unlocks) | Must Have |
| FR-045 | Transactions filterable by type (purchase/unlock) | Should Have |
| FR-046 | Each transaction shows: date, type, credits delta, balance after, description | Must Have |
| FR-047 | Payment history shows: package, amount, status, payment mode | Should Have |
| FR-048 | Admin dashboard shows platform-wide stats | Could Have |
| FR-049 | Admin can reconcile pending payments | Must Have |
| FR-050 | All credit movements are auditable via credit ledger | Must Have |

---

## 4. Task 2 — Business Rules & Scenarios

> Full document: [`docs/02_Business_Rules_Scenarios.md`](../02_Business_Rules_Scenarios.md)

### Business Rules Summary (15 Rules)

| ID | Rule | Category |
|----|------|----------|
| BR-001 | Users must register before purchasing credits | Auth |
| BR-002 | Credits purchased as full packages only | Credits |
| BR-003 | 10 credits per doctor profile unlock | Credits |
| BR-004 | Credits non-refundable once profile unlocked | Credits |
| BR-005 | Previously unlocked profiles are free to re-view | Credits |
| BR-006 | Credit balance cannot go below zero | Credits |
| BR-007 | Idempotency key required per payment | Payments |
| BR-008 | Credits added only after confirmed payment | Payments |
| BR-009 | Pending payments do not add credits | Payments |
| BR-010 | Failed payments add zero credits | Payments |
| BR-011 | Doctor contact details hidden until unlocked | Data Access |
| BR-012 | Search shows anonymized previews | Data Access |
| BR-013 | Only admins can reconcile pending payments | Administration |
| BR-014 | All credit movements logged in ledger | Audit |
| BR-015 | Demo payments carry mandatory disclaimer | Compliance |

### Scenarios Summary

---

#### SC-001 — Insufficient Credits

**Trigger:** User attempts to unlock a profile with < 10 credits  
**Expected:** HTTP 402, no credits deducted, no ledger entry, inline error + Buy Credits CTA  

```
Given user has 5 credits
When user sends POST /api/credits/unlock { "doctor_id": 42 }
Then status 402, balance unchanged, error message shown
```

---

#### SC-002 — Payment Failure

**Trigger:** Payment submitted with `payment_mode: "fail"`  
**Expected:** HTTP 200, status=failed, 0 credits added, Payment record created  

```
Given user has 50 credits, selects Growth package
When payment submitted with payment_mode="fail"
Then credits_added=0, balance unchanged, failure reason recorded
```

---

#### SC-003 — Payment Pending

**Trigger:** Payment submitted with `payment_mode: "pending"`  
**Expected:** HTTP 200, status=pending, 0 credits until admin reconciles  

```
Given payment_id=22 is pending
When admin calls POST /api/credits/reconcile/22
Then payment status becomes "success", credits added, ledger entry created
```

---

#### SC-004 — Empty Search Results

**Trigger:** Search with filter combination matching 0 doctors  
**Expected:** HTTP 200, empty array, empty state UI with suggestions  

```
GET /api/doctors?specialty=Neurology&city=Kochi
→ { "doctors": [], "total": 0, "total_pages": 0 }
```

---

#### SC-005 — Duplicate Payment Prevention

**Trigger:** Same idempotency key submitted twice  
**Expected:** Original payment result returned, no duplicate credits  

```
Given first purchase with key "idem-xyz" succeeded (100 credits)
When same request submitted again with key "idem-xyz"
Then original result returned, balance unchanged at 150 credits
```

---

## 5. Task 3 — Workflow Diagrams

> Full diagrams (Mermaid): [`docs/03_Workflow_Diagrams.md`](../03_Workflow_Diagrams.md)

### Diagram 1 — User Registration & Login

```
Visitor → Register/Login Form → Validate → JWT Token → Dashboard
                              ↓
                     Email Exists? → 400 Error
                     Wrong Password? → 401 Error
```

**Key nodes:** Form validation → Backend auth → JWT issuance → localStorage storage → redirect

### Diagram 2 — Credit Purchase Flow

```
Select Package → Choose Payment Mode → Generate Idempotency Key → Confirm
     ↓
Duplicate Key? → Return Original Result
     ↓
Payment Mode?
  success → Add Credits + Ledger → Show New Balance
  fail    → Record Failed Payment → Show Error
  pending → Record Pending → Admin Reconcile → Credits Added
```

### Diagram 3 — Doctor Search & Profile Unlock

```
Search/Filter → GET /api/doctors → Results or Empty State
     ↓
Click Doctor → GET /api/doctors/{id}
     ↓
Previously Unlocked? → Show Full Profile (free)
     ↓ No
Show Lock Icon → Click Unlock
     ↓
Balance >= 10? 
  No  → 402 Error → Buy Credits CTA
  Yes → Deduct 10 → Ledger → Reveal Contact Info
```

---

## 6. Task 4 — Wireframes

> Full wireframes (ASCII + annotations): [`docs/04_Wireframes.md`](../04_Wireframes.md)

### Screen 1 — Login / Registration

- Split tabs: Login | Register
- Email + Password fields with show/hide
- Demo credential fill buttons (reduces friction)
- Password strength indicator on register form
- Error feedback via toast notifications

### Screen 2 — Dashboard

- Left sidebar: logo, credit balance widget, navigation links
- 4 stat cards: balance, purchased, spent, unlocked count
- 3 quick action cards: Find Doctors, Buy Credits, Transactions
- Credit balance line chart (recharts)
- Recent activity list

### Screen 3 — Buy Credits

- Current balance banner
- Demo payment mode selector (3 scenarios)
- 4 package cards with pricing breakdown
- Purchase confirmation modal
- Result banner (success / failure / pending)

### Screen 4 — Doctor Search & Results

- Filter bar: search text, specialty, city, experience
- Doctor cards grid (3 columns): name, specialty, rating, hospital, locked contact
- Unlock button with credit cost
- Pagination controls
- Detailed profile page with full contact info

---

## 7. Task 5 — Assumptions & Client Questions

> Full document: [`docs/05_Assumptions_Questions.md`](../05_Assumptions_Questions.md)

### Key Assumptions (17 total)

| ID | Assumption |
|----|-----------|
| ASSUMP-001 | Credit-based model is sole monetization strategy |
| ASSUMP-002 | 10 credits per unlock is fixed (not specialty-variable) |
| ASSUMP-003 | Credits do not expire |
| ASSUMP-005 | All payments simulated for this assessment |
| ASSUMP-006 | All doctor data is fictional |
| ASSUMP-008 | B2C platform (not B2B/enterprise) |
| ASSUMP-011 | SQLite for demo; PostgreSQL for production |
| ASSUMP-013 | No KYC required for this assessment |

### Key Client Questions (20 total)

| ID | Question |
|----|---------|
| Q-001 | Is 10 credits/unlock price tested with users? |
| Q-002 | Should credits expire? |
| Q-006 | Who verifies doctor data quality? |
| Q-007 | Will doctors self-register? |
| Q-011 | Which payment gateway for production? |
| Q-013 | Is GST/invoicing required? |
| Q-016 | DPDP Act compliance requirements? |
| Q-019 | Expected peak concurrent users? |

---

## 8. Implementation Evidence

### Backend — Verified Working

```
e:\doctor data platform\backend\
├── app/
│   ├── main.py          ← FastAPI app, CORS, all 7 routers
│   ├── config.py        ← Pydantic settings
│   ├── database.py      ← SQLAlchemy engine + create_tables()
│   ├── dependencies.py  ← get_current_user, get_current_admin
│   ├── models/          ← 7 SQLAlchemy models
│   ├── schemas/         ← Pydantic request/response schemas
│   ├── repositories/    ← DB access layer
│   ├── services/        ← Business logic (auth, credit, doctor, dashboard)
│   ├── api/             ← 7 router modules
│   └── utils/security.py ← JWT + bcrypt
├── seed_data.py         ← VERIFIED: 31 doctors, 2 users, 4 packages created
├── tests/               ← 23 test cases (conftest + 4 test files)
└── doctor_platform.db   ← 126KB SQLite database
```

**Seed Data Verified:**
- `user@demo.com` / `Demo@1234` — 150 credits, regular user
- `admin@demo.com` / `Admin@1234` — 500 credits, admin
- 31 doctors: 10+ specialties, 8 cities (Bangalore, Mumbai, Delhi, Chennai, etc.)
- 4 packages: Starter (₹99/50cr), Growth (₹399/120cr), Professional (₹699/250cr), Enterprise (₹1499/650cr)

### Frontend — TypeScript Clean Build

```
e:\doctor data platform\frontend\
├── src/
│   ├── App.tsx               ← Router with ProtectedRoute, AdminRoute
│   ├── main.tsx              ← ReactDOM root, QueryClient, Providers
│   ├── types/index.ts        ← All TypeScript types (aligned with backend)
│   ├── lib/api.ts            ← Axios instance, JWT interceptor
│   ├── contexts/             ← AuthContext, ToastContext
│   ├── hooks/                ← useAuth, useDoctors, useCredits
│   ├── services/             ← authService, doctorService, creditService, transactionService
│   ├── pages/                ← 9 pages (login, register, dashboard, doctors, profile, credits, transactions, admin)
│   └── components/           ← layout (Sidebar, Header), dashboard, ui (Button, Card, Badge, etc.)
└── package.json
```

**TypeScript Build Status:** ✅ Zero errors — `npx tsc --noEmit` passes cleanly

### Business Scenarios in Code

**SC-001 (Insufficient Credits)** — [`backend/app/services/credit_service.py`](../../backend/app/services/credit_service.py):
```python
if user.credit_balance < cost:
    raise HTTPException(status_code=402, 
        detail=f"Insufficient credits. Need {cost}, have {user.credit_balance}")
```

**SC-002 (Payment Failure)** — payment record with `status="failed"`, `credits_added=0`

**SC-003 (Payment Pending)** — payment record with `status="pending"`, admin reconcile endpoint

**SC-004 (Empty Results)** — `GET /api/doctors` returns `{"doctors": [], "total": 0}` when no matches

**SC-005 (Idempotency)** — idempotency_key stored in payments table, duplicate checked before processing

---

## 9. How to Run the Application

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd "e:\doctor data platform\backend"

# Install dependencies
pip install -r requirements.txt

# Seed database (creates 31 doctors, 2 users)
python seed_data.py

# Start backend server
uvicorn app.main:app --reload --port 8000

# API Docs available at: http://localhost:8000/docs
```

### Frontend Setup

```bash
cd "e:\doctor data platform\frontend"

# Install dependencies
npm install

# Start development server
npm run dev

# App available at: http://localhost:5173
```

### Demo Credentials

| Role | Email | Password | Credits |
|------|-------|----------|---------|
| Regular User | user@demo.com | Demo@1234 | 150 |
| Admin | admin@demo.com | Admin@1234 | 500 |

### Testing Business Scenarios

| Scenario | How to Test |
|----------|-------------|
| SC-001 | Register new user (0 credits) → go to any doctor → try to unlock |
| SC-002 | Buy Credits page → select any package → choose ❌ Failed mode → Purchase |
| SC-003 | Buy Credits page → select any package → choose ⏳ Pending mode → Purchase |
| SC-004 | Doctor Search → type in search box → search for a non-existent specialty |
| SC-005 | (Backend) Same idempotency_key in two POST /api/credits/purchase requests |

---

## 10. Conclusion

This submission delivers a complete Doctor Data Platform fulfilling all five assessment tasks:

| Task | Deliverable | Mark |
|------|-------------|------|
| Task 1 — FRD | 50 requirements across 5 modules | /15 |
| Task 2 — Business Rules & Scenarios | 15 rules, 5 detailed scenarios with Gherkin | /10 |
| Task 3 — Workflow Diagrams | 3 Mermaid diagrams covering all flows | /10 |
| Task 4 — Wireframes | 4 screens with ASCII wireframes + design system | /10 |
| Task 5 — Assumptions & Questions | 17 assumptions, 20 client questions, risk register | /5 |

Beyond the five tasks, the submission includes a fully functional web application demonstrating that the requirements can actually be built — bringing the analysis to life with real, working software.

**Key differentiators:**
- All 5 business scenarios are **actually implemented** in backend code, not just documented
- Frontend TypeScript build **passes with zero errors**
- Database is **seeded and verified** with realistic fictional data
- Credit operations are **atomic and idempotent** (production-grade safety)
- The UI includes **demo scenario labels** (SC-002, SC-003) on the payment mode selector, making the assessment requirements immediately visible

---

*Doctor Data Platform — Multiplier AI Business Analyst Assessment*  
*All doctor data is fictional. All payments are simulated. No real charges are made.*
