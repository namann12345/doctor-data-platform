# Business Rules & Scenarios
## Doctor Data Platform — Multiplier AI Assessment (Task 2)

**Document Version:** 1.0  
**Date:** November 2026  
**Author:** Business Analysis Team  

---

## Overview

This document defines the core business rules governing the Doctor Data Platform's credit-based model, and details five critical business scenarios with complete specification, acceptance criteria, and exception handling.

---

## Business Rules Catalogue

| ID | Rule | Category | Priority |
|----|------|----------|----------|
| BR-001 | Users must register and verify email before purchasing credits | Authentication | High |
| BR-002 | Minimum credit purchase is 1 package (no fractional purchases) | Credits | High |
| BR-003 | Each doctor profile unlock costs exactly 10 credits | Credits | High |
| BR-004 | Credits are non-refundable once a profile is successfully unlocked | Credits | High |
| BR-005 | A previously unlocked profile can be re-viewed at no additional cost | Credits | High |
| BR-006 | Credit balance cannot go below zero; insufficient balance blocks unlock | Credits | High |
| BR-007 | Each payment must carry a unique idempotency key to prevent double-charging | Payments | Critical |
| BR-008 | Credits are added only after confirmed payment success | Payments | Critical |
| BR-009 | Pending payments must not credit the user's account until reconciled | Payments | Critical |
| BR-010 | Failed payments result in zero credits and no balance change | Payments | High |
| BR-011 | Doctor contact details (phone, email) are hidden until profile is unlocked | Data Access | High |
| BR-012 | Search results show anonymized previews regardless of unlock status | Data Access | Medium |
| BR-013 | Admin users can reconcile pending payments and force-add credits | Administration | High |
| BR-014 | All credit transactions must be logged in the ledger with before/after balances | Audit | High |
| BR-015 | Demo mode payments carry a mandatory disclaimer — no real money moves | Compliance | High |

---

## Scenario Specifications

---

### SC-001 — Insufficient Credits to Unlock Profile

**Scenario Title:** User attempts to unlock a doctor profile without sufficient credit balance

**Category:** Credit Management — Error Handling  
**Priority:** High  
**Linked Business Rules:** BR-003, BR-006

#### Context
The platform charges 10 credits per doctor profile unlock. A user may attempt to unlock a profile when their balance is below 10 credits. The system must handle this gracefully, block the action, and direct the user to purchase more credits.

#### Preconditions
- User is registered and authenticated
- User has an active session with a valid JWT token
- User's current credit balance is **less than 10 credits**
- The target doctor profile exists and is active in the system
- The doctor profile has **not** been previously unlocked by this user

#### Trigger
User clicks "Unlock Profile" or "View Full Details" button on a doctor card or profile page.

#### System Behavior (Step-by-Step)
1. User submits unlock request to `POST /api/credits/unlock` with `{ "doctor_id": <id> }`
2. Backend retrieves user's current `credit_balance` from database
3. System checks: `credit_balance < 10` → condition true
4. System **does not** deduct any credits
5. System **does not** create any ledger entry
6. System returns HTTP **402 Payment Required** with error detail
7. Frontend receives 402 response
8. Frontend displays inline error message on the profile page
9. Frontend shows "Buy Credits" call-to-action button
10. User is **not** redirected; they remain on the profile page

#### API Contract

**Request:**
```http
POST /api/credits/unlock
Authorization: Bearer <token>
Content-Type: application/json

{ "doctor_id": 42 }
```

**Response (402):**
```json
{
  "detail": "Insufficient credits. You need 10 credits to unlock this profile. Current balance: 5 credits."
}
```

#### User-Facing Message
> ⚠️ **Insufficient Credits**  
> You need **10 credits** to unlock this doctor's profile. Your current balance is **5 credits**.  
> [Buy Credits →]

#### Exception Handling
| Exception | Handling |
|-----------|----------|
| User balance exactly 0 | Same 402 response, message adjusted |
| Doctor ID does not exist | 404 Not Found (separate validation) |
| User not authenticated | 401 Unauthorized |
| Network error on frontend | Retry prompt shown |

#### Acceptance Criteria (Gherkin)
```gherkin
Scenario: User with 5 credits tries to unlock a profile costing 10 credits
  Given the user "alice@demo.com" has a credit balance of 5
  And doctor profile ID 42 exists and is not unlocked by alice
  When alice sends POST /api/credits/unlock with { "doctor_id": 42 }
  Then the response status code is 402
  And the response body contains "Insufficient credits"
  And alice's credit balance remains 5
  And no ledger entry is created
  And the doctor profile remains locked for alice
```

---

### SC-002 — Payment Failure — Credits Not Added

**Scenario Title:** Payment gateway returns failure; credits must not be added to user account

**Category:** Payment Processing — Failure Path  
**Priority:** Critical  
**Linked Business Rules:** BR-008, BR-010, BR-014

#### Context
Payments may fail due to card declines, network errors, or fraud detection. The platform must ensure that failed payments never result in credit additions. The failed payment must be recorded for audit purposes.

#### Preconditions
- User is authenticated
- User selects a valid credit package
- User submits payment with `payment_mode: "fail"` (simulated decline)
- An idempotency key is generated for this transaction

#### Trigger
User submits the purchase form with payment mode "fail" (or gateway returns failure code in production).

#### System Behavior (Step-by-Step)
1. User submits `POST /api/credits/purchase` with `payment_mode: "fail"`
2. System checks idempotency key — not a duplicate, proceed
3. System creates a **Payment** record with `status = "failed"`
4. System records `failure_reason = "Payment declined by gateway"`
5. System **does NOT** add any credits to user's balance
6. System **does NOT** create a CreditLedger entry
7. System returns HTTP **200 OK** with payment result indicating failure
8. Frontend displays failure notification: "Payment declined"
9. User's credit balance remains **unchanged**
10. Failed payment is visible in transaction history for reference

#### API Contract

**Request:**
```http
POST /api/credits/purchase
Authorization: Bearer <token>
Content-Type: application/json

{
  "package_id": 2,
  "payment_mode": "fail",
  "idempotency_key": "uuid-abc-123"
}
```

**Response (200):**
```json
{
  "payment_id": 15,
  "status": "failed",
  "credits_added": 0,
  "bonus_credits": 0,
  "new_balance": 50,
  "message": "Payment failed. No credits were added. Reason: Payment declined by gateway."
}
```

#### User-Facing Message
> ❌ **Payment Failed**  
> Your payment was declined. No credits were added to your account.  
> Please try again or use a different payment method.

#### Exception Handling
| Exception | Handling |
|-----------|----------|
| Duplicate idempotency key | Return original failed payment record (idempotent) |
| Package deactivated between selection and purchase | 400 Bad Request |
| DB write fails during payment record creation | 500 error, no partial records created |

#### Acceptance Criteria (Gherkin)
```gherkin
Scenario: User submits payment with failure mode
  Given the user "bob@demo.com" has a credit balance of 50
  And the "Growth" package costs ₹399 and grants 100 credits
  When bob submits a purchase with payment_mode "fail" and a unique idempotency_key
  Then the response status is 200
  And response.status equals "failed"
  And response.credits_added equals 0
  And bob's credit balance remains 50
  And a Payment record with status "failed" is created
  And no CreditLedger entry is created
```

---

### SC-003 — Payment Pending — Credits Not Immediately Added

**Scenario Title:** Payment gateway returns "pending" status; credits held until reconciliation

**Category:** Payment Processing — Pending State  
**Priority:** Critical  
**Linked Business Rules:** BR-008, BR-009, BR-013

#### Context
Some payment methods (bank transfers, UPI pending, wallet confirmations) may result in a "pending" state where the gateway has received the payment initiation but not yet confirmed the funds. Credits must NOT be added until the payment is confirmed. An admin reconciliation endpoint allows manual or automated resolution.

#### Preconditions
- User is authenticated
- User selects a credit package
- User submits payment with `payment_mode: "pending"`

#### Trigger
User initiates a payment that returns pending status.

#### System Behavior (Step-by-Step)
1. User submits `POST /api/credits/purchase` with `payment_mode: "pending"`
2. System creates a **Payment** record with `status = "pending"`
3. System **does NOT** add credits to user balance
4. System returns HTTP **200 OK** with pending status
5. Frontend shows informational message about pending state
6. User's credit balance remains unchanged
7. **[Admin Action]** Admin calls `POST /api/credits/reconcile/{payment_id}`
8. System verifies payment is in "pending" state
9. System updates payment `status → "success"`
10. System adds credits + bonus credits to user's balance
11. System creates CreditLedger entry with reconciliation note
12. System returns updated balance

#### API Contract — Purchase

**Response (200):**
```json
{
  "payment_id": 22,
  "status": "pending",
  "credits_added": 0,
  "bonus_credits": 0,
  "new_balance": 50,
  "message": "Payment is pending confirmation. Credits will be added once payment is verified."
}
```

#### API Contract — Reconciliation (Admin)

```http
POST /api/credits/reconcile/22
Authorization: Bearer <admin-token>
```

**Response:**
```json
{
  "message": "Payment 22 reconciled successfully. 100 credits added to user account.",
  "new_balance": 150
}
```

#### User-Facing Message (Pending)
> ⏳ **Payment Pending**  
> Your payment is awaiting confirmation. Credits will be added automatically once verified.  
> This typically takes 1-24 hours. No action needed.

#### Exception Handling
| Exception | Handling |
|-----------|----------|
| Reconcile called on already-success payment | 400 "Payment already processed" |
| Reconcile called on failed payment | 400 "Cannot reconcile a failed payment" |
| Non-admin tries to reconcile | 403 Forbidden |
| Payment not found | 404 Not Found |

#### Acceptance Criteria (Gherkin)
```gherkin
Scenario: Pending payment is reconciled by admin
  Given user "carol@demo.com" has balance 50
  And carol submits payment with payment_mode "pending" for 100-credit package
  Then carol's balance remains 50
  And a Payment with status "pending" and payment_id 22 is created
  When admin calls POST /api/credits/reconcile/22
  Then the payment status becomes "success"
  And carol's credit balance becomes 150
  And a CreditLedger entry with entry_type "purchase" is created
```

---

### SC-004 — No Search Results for Applied Filters

**Scenario Title:** Doctor search returns empty results for given filter combination

**Category:** Search & Discovery — Empty State  
**Priority:** Medium  
**Linked Business Rules:** None specific

#### Context
Users may apply filter combinations (specialty + city + experience) that return no matching doctors. The system must handle empty results gracefully, without errors, and guide the user to modify their search.

#### Preconditions
- User is authenticated
- Doctor database has 31 doctors seeded
- User applies a filter combination that matches zero doctors

#### Trigger
User searches with filters resulting in zero matches (e.g., Specialty: "Neurology" AND City: "Kochi").

#### System Behavior (Step-by-Step)
1. User applies search filters and submits request
2. Backend executes filtered query against `doctors` table
3. Query returns zero records
4. System returns HTTP **200 OK** with empty list (not 404)
5. Frontend receives `{ "doctors": [], "total": 0, "total_pages": 0 }`
6. Frontend renders "No Results" empty state component
7. Frontend suggests filter relaxation options
8. No credits are deducted

#### API Contract

**Request:**
```http
GET /api/doctors?specialty=Neurology&city=Kochi
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "doctors": [],
  "total": 0,
  "page": 1,
  "page_size": 12,
  "total_pages": 0
}
```

#### User-Facing Message
> 🔍 **No Doctors Found**  
> No doctors match your current filters. Try:
> - Removing the city filter
> - Selecting a different specialty
> - Expanding the experience range

#### Exception Handling
| Exception | Handling |
|-----------|----------|
| Invalid specialty value | 422 Validation Error |
| Invalid page number | Clamp to valid range |
| Database connection error | 500 with generic error message |

#### Acceptance Criteria (Gherkin)
```gherkin
Scenario: Search with no matching filters
  Given the platform has 31 doctors seeded
  And no doctors have specialty "Neurology" in city "Kochi"
  When user sends GET /api/doctors?specialty=Neurology&city=Kochi
  Then the response status is 200
  And response.total equals 0
  And response.doctors is an empty array
  And user's credit balance is unchanged
  And frontend shows "No Results" empty state
```

---

### SC-005 — Duplicate Payment Prevention (Idempotency)

**Scenario Title:** Duplicate payment submission is detected and rejected using idempotency key

**Category:** Payment Processing — Idempotency  
**Priority:** Critical  
**Linked Business Rules:** BR-007, BR-008

#### Context
Due to network retries, double-clicks, or browser refresh, a user may accidentally submit the same purchase request twice. The idempotency key prevents double-charging by detecting the duplicate and returning the original payment result.

#### Preconditions
- User is authenticated
- User has submitted a valid payment (success, fail, or pending)
- The original payment created a record with idempotency_key `"idem-xyz-456"`
- User retries the same request with the same idempotency_key

#### Trigger
Exact same purchase request is submitted with the same `idempotency_key` within any time window.

#### System Behavior (Step-by-Step)
1. User submits first purchase: `idempotency_key: "idem-xyz-456"` → succeeds, 100 credits added
2. User accidentally submits the same request again: `idempotency_key: "idem-xyz-456"`
3. System queries `payments` table: finds existing payment with this idempotency_key
4. System returns the **original payment result** without any new processing
5. No credits are added again
6. No new Payment record created
7. No new CreditLedger entry created
8. HTTP **200 OK** returned with original result

#### API Contract

**Second Request (duplicate):**
```http
POST /api/credits/purchase
Authorization: Bearer <token>
Content-Type: application/json

{
  "package_id": 2,
  "payment_mode": "success",
  "idempotency_key": "idem-xyz-456"
}
```

**Response (200) — returns original result:**
```json
{
  "payment_id": 10,
  "status": "success",
  "credits_added": 100,
  "bonus_credits": 20,
  "new_balance": 170,
  "message": "Credits already added (idempotent). Original transaction returned."
}
```

#### User-Facing Behavior
The user sees the same success confirmation they saw the first time. No error is shown. No duplicate credits are added. The UI may show "Payment already processed" in the status.

#### Exception Handling
| Exception | Handling |
|-----------|----------|
| Idempotency key exists but different package_id | 409 Conflict (mismatched idempotency) |
| Idempotency key collision from different user | Treated as new payment (user-scoped keys) |

#### Acceptance Criteria (Gherkin)
```gherkin
Scenario: Duplicate purchase request with same idempotency key
  Given user "dave@demo.com" has balance 50
  And dave submits purchase with idempotency_key "idem-xyz-456" and gets 100 credits
  And dave's balance is now 150
  When dave submits the same request again with idempotency_key "idem-xyz-456"
  Then the response status is 200
  And response.payment_id equals the original payment_id
  And dave's credit balance remains 150 (no double credit)
  And no new Payment record is created
  And no new CreditLedger entry is created
```

---

## Summary Matrix

| Scenario | HTTP Code | Credits Deducted | Ledger Entry | Business Rule |
|----------|-----------|-----------------|--------------|---------------|
| SC-001: Insufficient Credits | 402 | No | No | BR-003, BR-006 |
| SC-002: Payment Failure | 200 | No | No | BR-008, BR-010 |
| SC-003: Payment Pending | 200 | No | No (until reconciled) | BR-009, BR-013 |
| SC-004: Empty Search Results | 200 | No | No | N/A |
| SC-005: Duplicate Payment | 200 | No (idempotent) | No (original returned) | BR-007 |

---

*Document End — Doctor Data Platform Business Rules & Scenarios v1.0*
