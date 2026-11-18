# FUNCTIONAL REQUIREMENTS DOCUMENT (FRD)
## Doctor Data Platform — Multiplier AI Assessment

---

**Document Title:** Functional Requirements Document  
**Project:** Doctor Data Platform  
**Version:** 1.0  
**Date:** November 2026  
**Prepared By:** Business Analyst — Multiplier AI Assessment  
**Status:** Final Draft  

---

## Document Control

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 0.1 | Nov 2026 | BA Candidate | Initial draft |
| 0.2 | Nov 2026 | BA Candidate | Added acceptance criteria |
| 1.0 | Nov 2026 | BA Candidate | Final version for submission |

---

## Table of Contents

1. [Introduction & Purpose](#1-introduction--purpose)
2. [Project Scope](#2-project-scope)
3. [Stakeholders & User Personas](#3-stakeholders--user-personas)
4. [Module 1: User Registration & Login](#module-1-user-registration--login)
5. [Module 2: Credit Purchase & Payment](#module-2-credit-purchase--payment)
6. [Module 3: Doctor Search & Filters](#module-3-doctor-search--filters)
7. [Module 4: Doctor Details & Credit Deduction](#module-4-doctor-details--credit-deduction)
8. [Module 5: User Dashboard & Credit History](#module-5-user-dashboard--credit-history)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [Out-of-Scope Items](#10-out-of-scope-items)

---

## 1. Introduction & Purpose

The **Doctor Data Platform** is a web-based SaaS application that enables users to search, discover, and access detailed profiles of registered medical professionals across India. The platform operates on a **credit-based access model** where basic search results are free, but full doctor profile details (including contact, fees, and biography) require credit consumption.

This Functional Requirements Document (FRD) defines all system behaviors, business rules, acceptance criteria, and technical requirements needed to design, build, and validate the platform.

### 1.1 Business Problem Statement

Healthcare consumers, researchers, and institutional buyers need a reliable, structured database of verified medical professionals. Existing options are fragmented across multiple directories, hospital portals, and unverified listings. The Doctor Data Platform centralizes doctor information and monetizes premium data access through a scalable credit system.

### 1.2 Document Purpose

This document serves as the definitive specification for:
- Product and engineering teams to build the platform
- QA teams to design and execute test plans
- Stakeholders to validate requirements alignment

---

## 2. Project Scope

### 2.1 In-Scope

| Feature Area | Included |
|---|---|
| User Registration & Authentication | ✅ |
| JWT-based Session Management | ✅ |
| Credit Package Purchasing (Simulated Payment) | ✅ |
| Doctor Search with Filters | ✅ |
| Doctor Profile Unlock (Credit Deduction) | ✅ |
| User Dashboard & Credit History | ✅ |
| Credit Ledger & Audit Trail | ✅ |
| Admin Dashboard (Read-Only) | ✅ |

### 2.2 Out-of-Scope

| Feature | Reason |
|---|---|
| Real payment gateway integration | Assessment uses simulated payments |
| Doctor self-registration portal | Phase 2 feature |
| Appointment booking | Out of scope for MVP |
| Email/SMS notifications | Phase 2 |
| Mobile native apps | Web-only for MVP |
| Doctor data scraping or enrichment | Manual seeding for assessment |
| Multi-language support | English only for MVP |

---

## 3. Stakeholders & User Personas

### 3.1 Stakeholder List

| Stakeholder | Role | Interest |
|---|---|---|
| Product Owner | Multiplier AI | Business goals, feature prioritization |
| Backend Developer | Engineering Team | API specifications, data models |
| Frontend Developer | Engineering Team | UI behavior, API contracts |
| QA Engineer | Quality Assurance | Test criteria, edge cases |
| Business Analyst | Assessment Candidate | Requirements definition |
| End Users | Platform Consumers | Ease of use, value for credits |

### 3.2 User Personas

#### Persona 1: Riya Sharma — Patient Seeking Specialist

| Attribute | Detail |
|---|---|
| **Age** | 34 |
| **Role** | Software engineer, urban professional |
| **Goal** | Find a trusted cardiologist in Bangalore |
| **Pain Points** | Cannot verify doctor credentials; scattered information |
| **Behavior** | Searches by specialty + city, reads profile carefully before booking |
| **Tech Comfort** | High |
| **Credits Needed** | 1–3 unlocks per session |

#### Persona 2: Dr. Arvind Kapoor — Healthcare Researcher

| Attribute | Detail |
|---|---|
| **Age** | 45 |
| **Role** | Public health researcher at a university |
| **Goal** | Build a dataset of oncologists across Maharashtra |
| **Pain Points** | Needs bulk access; existing directories are incomplete |
| **Behavior** | Applies heavy filters, exports data, uses platform regularly |
| **Tech Comfort** | Medium-High |
| **Credits Needed** | 20–50 unlocks per month |

#### Persona 3: Admin User — Platform Administrator

| Attribute | Detail |
|---|---|
| **Age** | 28 |
| **Role** | Internal platform operations team |
| **Goal** | Monitor system usage, review transactions, oversee data quality |
| **Pain Points** | Needs real-time visibility into credit activity |
| **Behavior** | Accesses admin dashboard daily, monitors anomalies |
| **Tech Comfort** | High |
| **Credits Needed** | N/A (admin role) |

---

## MODULE 1: User Registration & Login

### Module Overview

| Field | Detail |
|---|---|
| **Module ID** | MOD-AUTH |
| **Module Name** | User Registration & Login |
| **Priority** | P0 — Critical |
| **Depends On** | None |

**Business Objective:** Enable secure, authenticated access to the platform. All users must register and log in to access any feature beyond the landing page.

**User Interaction:** Users navigate to `/register` or `/login`. Registration requires name, email, and password. Login requires email and password. On success, users receive a JWT and are redirected to `/dashboard`.

---

### FR-AUTH-001: User Registration

| Field | Detail |
|---|---|
| **Requirement ID** | FR-AUTH-001 |
| **Title** | New User Registration |
| **Priority** | P0 |
| **Status** | Active |

**Description:** The system shall allow new users to create an account by providing their full name, email address, and password. Upon successful registration, the system shall return a JWT access token and initialize the user's credit balance.

**Input Fields:**

| Field | Type | Validation | Required |
|---|---|---|---|
| `full_name` | String | Min 2 chars, max 100 chars, letters and spaces only | Yes |
| `email` | String (email) | Valid email format, unique in system | Yes |
| `password` | String | Min 8 chars, at least 1 uppercase, 1 number | Yes |

**System Behavior:**
1. User submits registration form
2. Frontend validates fields (client-side)
3. POST request sent to `/api/auth/register`
4. Backend validates all fields (server-side)
5. System checks for duplicate email in `users` table
6. If duplicate: return HTTP 409 with `error_code: EMAIL_ALREADY_EXISTS`
7. Password hashed using bcrypt (cost factor 12)
8. New user record created with `credit_balance = 0`, `role = "user"`, `is_active = true`
9. JWT token generated with user ID and email as claims
10. Response: HTTP 201 with token and user object

**Functional Requirements:**

| FR-ID | Description |
|---|---|
| FR-AUTH-001.1 | System shall collect full_name, email, and password on registration |
| FR-AUTH-001.2 | System shall validate email format using RFC 5322 standard |
| FR-AUTH-001.3 | System shall reject registration if email already exists |
| FR-AUTH-001.4 | System shall hash passwords using bcrypt before storage |
| FR-AUTH-001.5 | System shall initialize credit_balance to 0 on registration |
| FR-AUTH-001.6 | System shall return JWT on successful registration |
| FR-AUTH-001.7 | System shall not store plaintext passwords |

**Business Rules:**

| BR-ID | Rule |
|---|---|
| BR-AUTH-001 | Each email address may only be associated with one user account |
| BR-AUTH-002 | Passwords must be bcrypt hashed with minimum cost factor of 10 |
| BR-AUTH-003 | New accounts receive role = "user" by default |
| BR-AUTH-004 | New accounts receive credit_balance = 0 at creation |

**Acceptance Criteria:**

```gherkin
Scenario: Successful registration
  Given a user is on the registration page
  When they submit full_name="Riya Sharma", email="riya@example.com", password="SecurePass1"
  Then the system returns HTTP 201
  And a JWT token is returned
  And user is redirected to /dashboard
  And credit_balance is 0

Scenario: Duplicate email registration
  Given a user with email "riya@example.com" already exists
  When a new user attempts to register with the same email
  Then the system returns HTTP 409
  And error_code is "EMAIL_ALREADY_EXISTS"
  And no new account is created

Scenario: Invalid password format
  Given a user is on the registration page
  When they submit password="abc" (too short, no uppercase, no number)
  Then the system returns HTTP 422
  And error message indicates password requirements
```

**Exception Handling:**

| Scenario | HTTP Code | Error Code | User Message |
|---|---|---|---|
| Email already registered | 409 | EMAIL_ALREADY_EXISTS | "An account with this email already exists." |
| Invalid email format | 422 | VALIDATION_ERROR | "Please enter a valid email address." |
| Weak password | 422 | WEAK_PASSWORD | "Password must be at least 8 characters with 1 uppercase and 1 number." |
| Server error | 500 | INTERNAL_ERROR | "Registration failed. Please try again." |

---

### FR-AUTH-002: User Login

| Field | Detail |
|---|---|
| **Requirement ID** | FR-AUTH-002 |
| **Title** | Existing User Login |
| **Priority** | P0 |

**Description:** The system shall allow registered users to authenticate using email and password, returning a JWT token on success.

**Input Fields:**

| Field | Type | Validation | Required |
|---|---|---|---|
| `email` | String (email) | Valid format | Yes |
| `password` | String | Non-empty | Yes |

**System Behavior:**
1. User submits login form
2. POST to `/api/auth/login`
3. System looks up user by email
4. If not found: return HTTP 401
5. System verifies bcrypt hash of submitted password against stored hash
6. If mismatch: return HTTP 401 (generic message, do not reveal which field failed)
7. If match: generate JWT with 7-day expiry
8. Return HTTP 200 with token and user summary

**Functional Requirements:**

| FR-ID | Description |
|---|---|
| FR-AUTH-002.1 | System shall authenticate user by email and password |
| FR-AUTH-002.2 | System shall use bcrypt to verify password |
| FR-AUTH-002.3 | System shall return generic error message on failure (no field-level hints) |
| FR-AUTH-002.4 | System shall return JWT on successful login |
| FR-AUTH-002.5 | JWT shall expire after 10080 minutes (7 days) |

**Business Rules:**

| BR-ID | Rule |
|---|---|
| BR-AUTH-005 | Failed login shall not reveal whether the email or password was incorrect |
| BR-AUTH-006 | JWT tokens expire after 7 days of inactivity |
| BR-AUTH-007 | Inactive accounts (is_active=false) cannot log in |

**Acceptance Criteria:**

```gherkin
Scenario: Successful login
  Given a registered user with email "riya@example.com" and password "SecurePass1"
  When the user submits valid credentials
  Then HTTP 200 is returned
  And a JWT token is included in the response
  And user is redirected to /dashboard

Scenario: Failed login with wrong password
  Given a registered user with email "riya@example.com"
  When the user submits incorrect password "WrongPass1"
  Then HTTP 401 is returned
  And error_code is "INVALID_CREDENTIALS"
  And no token is returned

Scenario: Login with non-existent email
  Given no user exists with email "ghost@example.com"
  When login is attempted with that email
  Then HTTP 401 is returned
  And error_code is "INVALID_CREDENTIALS"
```

---

### FR-AUTH-003 through FR-AUTH-012: Additional Auth Requirements

| FR-ID | Title | Description |
|---|---|---|
| FR-AUTH-003 | JWT Validation Middleware | All protected endpoints must validate JWT in Authorization header |
| FR-AUTH-004 | Get Current User | GET /api/auth/me returns user object for authenticated user |
| FR-AUTH-005 | Token Expiry Handling | Expired tokens return HTTP 401 with error_code: TOKEN_EXPIRED |
| FR-AUTH-006 | Invalid Token Handling | Malformed tokens return HTTP 401 with error_code: INVALID_TOKEN |
| FR-AUTH-007 | Missing Token Handling | Requests to protected routes without token return HTTP 401 |
| FR-AUTH-008 | Password Change | Authenticated user can change password by providing current + new password |
| FR-AUTH-009 | Profile Update | Authenticated user can update full_name via PUT /api/profile |
| FR-AUTH-010 | Role-Based Access | Admin role required for /api/admin/* endpoints |
| FR-AUTH-011 | Account Deactivation Guard | is_active=false users cannot authenticate |
| FR-AUTH-012 | Password Hashing Standard | bcrypt with minimum cost factor 12 required |

---

## MODULE 2: Credit Purchase & Payment

### Module Overview

| Field | Detail |
|---|---|
| **Module ID** | MOD-CRED |
| **Module Name** | Credit Purchase & Payment |
| **Priority** | P0 — Critical |
| **Depends On** | MOD-AUTH |

**Business Objective:** Enable users to purchase credits via a simulated payment flow. Credits are the currency of the platform, required to access full doctor profiles. The payment flow must be atomic, idempotent, and audit-traceable.

**Credit Packages:**

| Package | Credits | Price (INR) | Value |
|---|---|---|---|
| Starter | 50 | ₹499 | Best for casual users |
| Growth | 150 | ₹999 | Most popular |
| Professional | 400 | ₹1,999 | For regular researchers |
| Enterprise | 1,000 | ₹3,999 | For institutional buyers |

---

### FR-CRED-001: View Credit Packages

| FR-ID | Description |
|---|---|
| FR-CRED-001 | System shall display all available credit packages with name, credit amount, price, and value label |
| FR-CRED-001.1 | Packages shall be fetched from GET /api/credits/packages |
| FR-CRED-001.2 | Packages shall show price in INR |
| FR-CRED-001.3 | System shall highlight a "Most Popular" package |

---

### FR-CRED-002: Initiate Credit Purchase

| Field | Detail |
|---|---|
| **Requirement ID** | FR-CRED-002 |
| **Title** | Initiate Credit Purchase |
| **Priority** | P0 |

**Description:** When a user selects a credit package and initiates purchase, the system shall generate a unique idempotency key, create a pending payment record, and proceed to simulate payment.

**Input Fields:**

| Field | Type | Validation | Required |
|---|---|---|---|
| `package_id` | Integer | Must be valid existing package ID | Yes |
| `payment_mode` | String (enum) | "success", "fail", "pending" | Yes |
| `idempotency_key` | String (UUID) | UUID v4, unique per request | Yes |

**System Behavior:**
1. User selects package and payment_mode
2. Frontend generates UUID v4 as `idempotency_key`
3. POST to `/api/credits/purchase`
4. Backend checks if `idempotency_key` already exists in payments table
5. If exists: return the existing payment result (idempotent response)
6. If new: create payment record with status = "pending"
7. Simulate payment based on `payment_mode`:
   - `"success"`: Atomic credit addition + ledger entry + transaction record. Status → "completed"
   - `"fail"`: No credits added. Status → "failed"
   - `"pending"`: No credits added. Status → "pending" (requires manual reconciliation)
8. Return HTTP 200 with payment result

**Functional Requirements:**

| FR-ID | Description |
|---|---|
| FR-CRED-002.1 | System shall validate package_id exists before processing |
| FR-CRED-002.2 | System shall require and validate idempotency_key (UUID format) |
| FR-CRED-002.3 | System shall check for duplicate idempotency_key before processing |
| FR-CRED-002.4 | System shall create a payment record with status "pending" before processing |
| FR-CRED-002.5 | System shall add credits ONLY when payment_mode = "success" |
| FR-CRED-002.6 | Credit addition, ledger entry, and transaction record shall be atomic (single DB transaction) |
| FR-CRED-002.7 | System shall NOT add credits when payment_mode = "fail" |
| FR-CRED-002.8 | System shall NOT add credits when payment_mode = "pending" |

**Business Rules:**

| BR-ID | Rule |
|---|---|
| BR-CRED-001 | Credits are only added after confirmed successful payment |
| BR-CRED-002 | Each purchase request must carry a unique idempotency_key |
| BR-CRED-003 | Duplicate idempotency_key returns existing result without reprocessing |
| BR-CRED-004 | Credit addition and ledger recording must succeed together or fail together |
| BR-CRED-005 | Failed payments must not add any credits |
| BR-CRED-006 | Pending payments must be manually or automatically reconciled |
| BR-CRED-007 | All credit transactions must be recorded in the credit_ledger table |

**Acceptance Criteria:**

```gherkin
Scenario: Successful credit purchase
  Given a logged-in user with current_balance = 20
  And a valid package (Growth: 150 credits, ₹999)
  When user submits purchase with payment_mode = "success"
  Then HTTP 200 is returned
  And user.credit_balance increases by 150 to 170
  And a credit_ledger entry of type "credit" is created
  And a transaction record is created with status "completed"
  And payment record shows status "completed"

Scenario: Failed payment — no credits added
  Given a logged-in user with current_balance = 20
  When user submits purchase with payment_mode = "fail"
  Then HTTP 200 is returned with payment_status = "failed"
  And user.credit_balance remains 20
  And no credit_ledger entry is created
  And no credits are added

Scenario: Duplicate payment prevention
  Given a purchase was already processed with idempotency_key = "abc-123"
  When a second request is submitted with the same idempotency_key = "abc-123"
  Then HTTP 200 is returned with the original payment result
  And no duplicate credits are added
  And no new payment record is created
```

---

### FR-CRED-003 through FR-CRED-015: Additional Credit Requirements

| FR-ID | Title | Description |
|---|---|---|
| FR-CRED-003 | Credit Balance Retrieval | GET /api/credits/balance returns current user balance |
| FR-CRED-004 | Credit History | GET /api/credits/history returns paginated ledger entries |
| FR-CRED-005 | Transaction History | GET /api/transactions returns all user transactions |
| FR-CRED-006 | Transaction Detail | GET /api/transactions/{id} returns single transaction |
| FR-CRED-007 | Payment Status Display | Frontend shows payment result (success/fail/pending) with appropriate messaging |
| FR-CRED-008 | Atomic Credit Deduction | Unlocking a doctor profile deducts credits atomically |
| FR-CRED-009 | Ledger Debit Recording | Each unlock creates a "debit" entry in credit_ledger |
| FR-CRED-010 | Balance Guard on Purchase | System rejects unlock (not purchase) if balance insufficient |
| FR-CRED-011 | Credit Package Admin | Admin can view all packages; editing is out of scope for MVP |
| FR-CRED-012 | Credit Reconciliation Flag | Pending payments flagged for manual review by admin |
| FR-CRED-013 | Credit Cost Config | CREDIT_COST_PER_PROFILE = 10 credits (env variable) |
| FR-CRED-014 | No Negative Balance | System must never allow credit_balance to go below 0 |
| FR-CRED-015 | Currency Display | All prices displayed in Indian Rupees (INR, ₹) |

---

## MODULE 3: Doctor Search & Filters

### Module Overview

| Field | Detail |
|---|---|
| **Module ID** | MOD-SRCH |
| **Module Name** | Doctor Search & Filters |
| **Priority** | P0 — Critical |
| **Depends On** | MOD-AUTH |

**Business Objective:** Allow users to discover doctors using search and filter functionality. Search is free and does not consume credits. Users see basic doctor information (name, specialty, city, experience) in search results, with full details requiring credit unlock.

---

### FR-SRCH-001: Text Search

| Field | Detail |
|---|---|
| **Requirement ID** | FR-SRCH-001 |
| **Title** | Doctor Text Search |
| **Priority** | P0 |

**Description:** Users shall be able to search for doctors by name or specialty using a text search input. Search is performed via a real database query on the backend.

**Input Fields:**

| Field | Type | Validation | Required |
|---|---|---|---|
| `search` | String (query param) | Optional, max 200 chars | No |
| `specialty` | String (query param) | Optional, must match valid specialty | No |
| `city` | String (query param) | Optional | No |
| `page` | Integer | Min 1, default 1 | No |
| `page_size` | Integer | Min 5, max 50, default 10 | No |

**System Behavior:**
1. User enters search term or selects filters
2. GET request to `/api/doctors?search=X&specialty=Y&city=Z&page=1`
3. Backend executes filtered database query
4. Results returned as paginated list
5. Each result includes: id, name, specialty, city, experience, is_unlocked flag
6. `is_unlocked` flag indicates if current user has already unlocked this doctor

**Functional Requirements:**

| FR-ID | Description |
|---|---|
| FR-SRCH-001.1 | System shall support text search across doctor name and specialty fields |
| FR-SRCH-001.2 | Search shall be case-insensitive |
| FR-SRCH-001.3 | System shall support filtering by specialty |
| FR-SRCH-001.4 | System shall support filtering by city |
| FR-SRCH-001.5 | System shall support combined search and filter |
| FR-SRCH-001.6 | Results shall be paginated (default 10 per page) |
| FR-SRCH-001.7 | Results shall show total count and pagination metadata |
| FR-SRCH-001.8 | Search shall not consume credits |
| FR-SRCH-001.9 | Each result card shall include is_unlocked flag for the current user |
| FR-SRCH-001.10 | Empty search with no filters returns all doctors (paginated) |

**Business Rules:**

| BR-ID | Rule |
|---|---|
| BR-SRCH-001 | Doctor search is free and does not consume credits |
| BR-SRCH-002 | Search results show name, specialty, city, years of experience, availability |
| BR-SRCH-003 | Full profile details (contact, fee, biography) require credit unlock |
| BR-SRCH-004 | Search must query actual backend database, not static/mock data |
| BR-SRCH-005 | Results must include pagination metadata (total, page, page_size) |

**Acceptance Criteria:**

```gherkin
Scenario: Successful doctor search
  Given a logged-in user
  When they search for "cardiologist" with city = "Mumbai"
  Then results are returned with matching doctors
  And each result shows name, specialty, city, experience
  And HTTP 200 is returned
  And credits are NOT deducted

Scenario: No results found
  Given a logged-in user
  When they search for specialty = "Astro-medicine"
  Then HTTP 200 is returned with empty results array
  And total_count = 0
  And UI displays "No doctors found matching your criteria"

Scenario: Pagination
  Given 25 doctors match search criteria
  When user requests page=2 with page_size=10
  Then results contain doctors 11-20
  And response includes total=25, page=2, page_size=10, total_pages=3
```

---

### FR-SRCH-002 through FR-SRCH-010: Additional Search Requirements

| FR-ID | Title | Description |
|---|---|---|
| FR-SRCH-002 | Specialty Filter | System shall provide dropdown of available specialties |
| FR-SRCH-003 | City Filter | System shall provide dropdown or autocomplete for city |
| FR-SRCH-004 | Experience Filter | System shall support filtering by years of experience range |
| FR-SRCH-005 | Combined Filters | System shall support combining multiple filters simultaneously |
| FR-SRCH-006 | Filter Reset | System shall provide "Clear Filters" button to reset all filters |
| FR-SRCH-007 | URL State | Filter and search state shall be reflected in the URL query params |
| FR-SRCH-008 | Result Count | System shall display "X doctors found" in the results header |
| FR-SRCH-009 | Availability Filter | System shall support filtering by availability (available_now flag) |
| FR-SRCH-010 | Unlocked Indicator | Search results shall visually distinguish already-unlocked profiles |

---

## MODULE 4: Doctor Details & Credit Deduction

### Module Overview

| Field | Detail |
|---|---|
| **Module ID** | MOD-DOCV |
| **Module Name** | Doctor Details & Credit Deduction |
| **Priority** | P0 — Critical |
| **Depends On** | MOD-AUTH, MOD-CRED, MOD-SRCH |

**Business Objective:** When a user views a doctor's full profile, the system deducts 10 credits from their balance. If the user has already unlocked the same doctor, no additional charges apply. This is the core monetization mechanism of the platform.

---

### FR-DOCV-001: View Doctor Profile (Locked State)

| Field | Detail |
|---|---|
| **Requirement ID** | FR-DOCV-001 |
| **Title** | Doctor Profile Locked State |
| **Priority** | P0 |

**Description:** When a user visits a doctor's detail page and has not previously unlocked the profile, the system shall display a locked state showing basic information and an "Unlock for 10 Credits" prompt.

**System Behavior:**
1. User clicks doctor card in search results
2. GET request to `/api/doctors/{id}`
3. Backend checks `doctor_unlocks` table for record matching (user_id, doctor_id)
4. If no record: return doctor with `is_unlocked = false` and limited data
5. Frontend renders locked profile state

**Acceptance Criteria:**

```gherkin
Scenario: Viewing locked doctor profile
  Given a logged-in user who has NOT unlocked doctor ID 42
  When they navigate to /doctors/42
  Then HTTP 200 is returned
  And is_unlocked = false
  And full details (phone, email, fee, bio) are hidden/masked
  And "Unlock for 10 Credits" button is displayed
```

---

### FR-DOCV-002: Unlock Doctor Profile

| Field | Detail |
|---|---|
| **Requirement ID** | FR-DOCV-002 |
| **Title** | Unlock Doctor Profile via Credit Deduction |
| **Priority** | P0 |

**Description:** When a user confirms they want to unlock a doctor profile, the system atomically deducts 10 credits from their balance, creates an unlock record, records a ledger debit entry, and returns the full doctor details.

**Input Fields:**

| Field | Type | Validation | Required |
|---|---|---|---|
| `doctor_id` (path) | Integer | Must be valid doctor ID | Yes |
| `Authorization` (header) | String (JWT) | Valid, non-expired JWT | Yes |

**System Behavior:**
1. User clicks "Unlock for 10 Credits" and confirms
2. POST to `/api/doctors/{id}/unlock`
3. Backend authenticates user via JWT
4. Backend checks `doctor_unlocks` for existing unlock record (user_id, doctor_id)
5. If already unlocked: return full profile with `is_unlocked = true`, no charge
6. If not unlocked: check `user.credit_balance >= CREDIT_COST_PER_PROFILE (10)`
7. If insufficient balance: return HTTP 402 with `INSUFFICIENT_CREDITS`
8. If sufficient balance: begin DB transaction
   - Deduct 10 credits from `users.credit_balance`
   - Insert record into `doctor_unlocks` (user_id, doctor_id, credits_spent=10)
   - Insert debit entry into `credit_ledger`
9. Commit transaction
10. Return HTTP 200 with full doctor profile

**Functional Requirements:**

| FR-ID | Description |
|---|---|
| FR-DOCV-002.1 | System shall check for existing unlock before deducting credits |
| FR-DOCV-002.2 | System shall verify credit balance >= 10 before unlocking |
| FR-DOCV-002.3 | System shall reject unlock with HTTP 402 if balance < 10 |
| FR-DOCV-002.4 | Credit deduction and unlock record creation shall be atomic |
| FR-DOCV-002.5 | Unlock record must be created in doctor_unlocks table |
| FR-DOCV-002.6 | Credit debit must be recorded in credit_ledger table |
| FR-DOCV-002.7 | Previously unlocked profiles must be accessible without re-charging |
| FR-DOCV-002.8 | Full doctor details returned only after successful unlock or existing unlock |

**Business Rules:**

| BR-ID | Rule |
|---|---|
| BR-DOCV-001 | Unlocking a doctor profile costs exactly 10 credits |
| BR-DOCV-002 | Credits are deducted atomically in a single database transaction |
| BR-DOCV-003 | A previously unlocked profile can be accessed again at no charge |
| BR-DOCV-004 | The system must reject unlock if credit_balance < 10 |
| BR-DOCV-005 | No unlock record shall be created if credit deduction fails |
| BR-DOCV-006 | No credit deduction shall occur if unlock record already exists |
| BR-DOCV-007 | Credit balance must never go negative |

**Acceptance Criteria:**

```gherkin
Scenario: Successful first-time unlock
  Given a logged-in user with credit_balance = 50
  And doctor with ID 10 has not been unlocked by this user
  When user confirms unlock by calling POST /api/doctors/10/unlock
  Then HTTP 200 is returned
  And is_unlocked = true in response
  And user.credit_balance decreases to 40
  And a doctor_unlocks record is created for (user_id, doctor_id=10)
  And a credit_ledger debit entry of -10 is recorded

Scenario: Insufficient credits
  Given a logged-in user with credit_balance = 5
  And doctor with ID 10 has not been unlocked by this user
  When user attempts to unlock doctor 10
  Then HTTP 402 is returned
  And error_code = "INSUFFICIENT_CREDITS"
  And user.credit_balance remains 5
  And no unlock record is created
  And no ledger entry is created

Scenario: Re-accessing previously unlocked profile
  Given a logged-in user who previously unlocked doctor ID 10
  And user has credit_balance = 5
  When user calls POST /api/doctors/10/unlock or GET /api/doctors/10
  Then HTTP 200 is returned
  And full profile is returned
  And credit_balance remains 5 (no deduction)

Scenario: Failed unlock due to system error
  Given a logged-in user with credit_balance = 50
  When the database transaction fails during unlock
  Then the entire transaction is rolled back
  And credit_balance remains 50
  And no unlock record is created
  And HTTP 500 is returned
```

---

### FR-DOCV-003 through FR-DOCV-012: Additional Doctor View Requirements

| FR-ID | Title | Description |
|---|---|---|
| FR-DOCV-003 | Full Profile Fields | Full profile includes: qualification, experience, specialty, hospital, phone, email, consultation_fee, biography, available_now |
| FR-DOCV-004 | Locked Profile Fields | Locked profile shows: name, specialty, city, experience, available_now. Hides: phone, email, fee, biography |
| FR-DOCV-005 | Unlocked Doctor List | GET /api/doctors/unlocked returns all doctors unlocked by current user |
| FR-DOCV-006 | Doctor Availability | available_now flag shows whether doctor is marked as currently available |
| FR-DOCV-007 | Confirmation Modal | Frontend shall show confirmation modal before deducting credits |
| FR-DOCV-008 | Post-Unlock Navigation | After unlock, user stays on doctor profile page with full details visible |
| FR-DOCV-009 | Insufficient Credits Redirect | On 402 response, frontend shows "Buy Credits" button linking to /credits |
| FR-DOCV-010 | Unlock History | Unlock date and credits_spent recorded in doctor_unlocks table |
| FR-DOCV-011 | Real-Time Balance Update | Frontend credit balance display updates immediately after unlock |
| FR-DOCV-012 | Error Recovery | On failed unlock (500), frontend shows error and preserves state |

---

## MODULE 5: User Dashboard & Credit History

### Module Overview

| Field | Detail |
|---|---|
| **Module ID** | MOD-DASH |
| **Module Name** | User Dashboard & Credit History |
| **Priority** | P1 — High |
| **Depends On** | MOD-AUTH, MOD-CRED, MOD-DOCV |

**Business Objective:** Provide users with a centralized view of their platform activity including credit balance, spending history, unlocked doctors, and quick action shortcuts. All data must be fetched from real backend APIs.

---

### FR-DASH-001: Dashboard Summary

| Field | Detail |
|---|---|
| **Requirement ID** | FR-DASH-001 |
| **Title** | Dashboard Summary Data |
| **Priority** | P1 |

**Description:** The dashboard shall display a real-time summary of the user's platform activity including credit balance, number of unlocked doctors, total credits spent, and recent activity.

**System Behavior:**
1. User navigates to `/dashboard`
2. Frontend calls GET `/api/dashboard/summary`
3. Backend aggregates: credit_balance, total_unlocked_doctors, total_credits_spent, recent_unlocks
4. Data returned and displayed in dashboard cards

**Functional Requirements:**

| FR-ID | Description |
|---|---|
| FR-DASH-001.1 | Dashboard shall display current credit_balance |
| FR-DASH-001.2 | Dashboard shall display total number of doctors unlocked |
| FR-DASH-001.3 | Dashboard shall display total credits spent |
| FR-DASH-001.4 | Dashboard shall display recent unlock activity list |
| FR-DASH-001.5 | Dashboard data shall come from real backend API calls |
| FR-DASH-001.6 | Dashboard shall show credit trend chart |
| FR-DASH-001.7 | Dashboard shall provide Quick Action links (Buy Credits, Search Doctors) |

**Business Rules:**

| BR-ID | Rule |
|---|---|
| BR-DASH-001 | All dashboard metrics must reflect real backend data |
| BR-DASH-002 | Credit balance shown must match the value in users.credit_balance |
| BR-DASH-003 | Unlock count must match doctor_unlocks records for the user |
| BR-DASH-004 | Credit spent must be calculated from credit_ledger debit entries |

**Acceptance Criteria:**

```gherkin
Scenario: Dashboard data accuracy
  Given a user who has purchased 150 credits and unlocked 3 doctors
  When they navigate to /dashboard
  Then credit_balance shown = (150 - 30) = 120
  And unlocked_doctors count = 3
  And total_credits_spent = 30
  And recent activity shows the 3 unlocked doctors

Scenario: Real-time balance update
  Given a user is on the dashboard with balance = 50
  When they purchase 150 more credits in another tab
  And they refresh the dashboard
  Then credit_balance updates to 200
```

---

### FR-DASH-002 through FR-DASH-010: Additional Dashboard Requirements

| FR-ID | Title | Description |
|---|---|---|
| FR-DASH-002 | Activity Feed | GET /api/dashboard/activity returns recent transactions and unlocks |
| FR-DASH-003 | Credit History Page | Dedicated page shows full paginated credit_ledger with dates |
| FR-DASH-004 | Transaction History Page | Full paginated list of all payment transactions |
| FR-DASH-005 | Unlocked Doctors Page | List of all doctors the user has unlocked with unlock date |
| FR-DASH-006 | Navigation Links | Dashboard provides direct links to all major features |
| FR-DASH-007 | Credit Chart | Visual chart of credit inflow/outflow over time |
| FR-DASH-008 | Profile Management | User can view and update their profile from dashboard |
| FR-DASH-009 | Password Change | User can change password from profile settings |
| FR-DASH-010 | Empty States | All lists show appropriate empty state when no data exists |

---

## 9. Non-Functional Requirements

### 9.1 Performance Requirements

| NFR-ID | Requirement | Target |
|---|---|---|
| NFR-PERF-001 | API response time (95th percentile) | < 500ms |
| NFR-PERF-002 | Search results return time | < 1 second |
| NFR-PERF-003 | Dashboard load time | < 2 seconds |
| NFR-PERF-004 | Credit purchase completion | < 3 seconds |
| NFR-PERF-005 | Concurrent user support | 100+ concurrent users |

### 9.2 Security Requirements

| NFR-ID | Requirement |
|---|---|
| NFR-SEC-001 | Passwords stored using bcrypt (cost factor >= 12) |
| NFR-SEC-002 | JWT tokens used for all authentication |
| NFR-SEC-003 | All API endpoints requiring auth must validate JWT |
| NFR-SEC-004 | No plaintext passwords stored or logged |
| NFR-SEC-005 | SQL injection prevention via parameterized queries (ORM) |
| NFR-SEC-006 | CORS configuration to allow only trusted origins |
| NFR-SEC-007 | Credit deduction protected from race conditions via DB transactions |

### 9.3 Usability Requirements

| NFR-ID | Requirement |
|---|---|
| NFR-USE-001 | Error messages must be user-friendly and actionable |
| NFR-USE-002 | Credit balance always visible in navigation header |
| NFR-USE-003 | Insufficient credits state must clearly show shortfall and Buy Credits CTA |
| NFR-USE-004 | Confirmation modal required before credit deduction |
| NFR-USE-005 | Mobile-responsive design |

### 9.4 Reliability Requirements

| NFR-ID | Requirement |
|---|---|
| NFR-REL-001 | Credit operations must be atomic — no partial state |
| NFR-REL-002 | System uptime target: 99.5% |
| NFR-REL-003 | Failed transactions must be logged for reconciliation |
| NFR-REL-004 | Database must be ACID-compliant |

---

## 10. Out-of-Scope Items

| Item | Notes |
|---|---|
| Real payment gateway | Simulated for MVP |
| Doctor registration portal | Phase 2 |
| Appointment/booking system | Out of scope |
| Email notifications | Phase 2 |
| SMS/OTP verification | Phase 2 |
| Native mobile apps | Web only for MVP |
| Multi-language (i18n) | English only for MVP |
| Credit expiry | Phase 2 |
| Refund processing | Manual process, not automated |
| Data export (CSV/PDF) | Phase 2 |
| Doctor ratings/reviews | Phase 2 |

---

*Document End — FRD v1.0*
