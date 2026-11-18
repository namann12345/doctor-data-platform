# Workflow Diagrams
## Doctor Data Platform — Multiplier AI Assessment (Task 3)

**Document Version:** 1.0  
**Date:** November 2026  

---

## Diagram 1 — User Registration & Login Flow

```mermaid
flowchart TD
    A([User Visits Platform]) --> B{Has Account?}
    B -- No --> C[Click Register]
    B -- Yes --> D[Click Login]

    C --> E[Fill Registration Form\nName, Email, Password]
    E --> F{Validate Input}
    F -- Invalid --> G[Show Validation Errors]
    G --> E
    F -- Valid --> H[POST /api/auth/register]
    H --> I{Email Already\nRegistered?}
    I -- Yes --> J[Return 400 Error\nEmail already in use]
    J --> E
    I -- No --> K[Hash Password\nCreate User Record]
    K --> L[Set credit_balance = 0]
    L --> M[Generate JWT Token]
    M --> N[Return TokenResponse\naccess_token + user info]
    N --> O[Store Token in\nLocalStorage]
    O --> P([Redirect to Dashboard])

    D --> Q[Fill Login Form\nEmail + Password]
    Q --> R[POST /api/auth/login\nform-data format]
    R --> S{User Found?}
    S -- No --> T[Return 401 Unauthorized]
    T --> U[Show Error Message]
    U --> Q
    S -- Yes --> V{Password\nMatches?}
    V -- No --> T
    V -- Yes --> W[Generate JWT Token\n24hr expiry]
    W --> X[Return TokenResponse]
    X --> Y[Store ddp_token\nin localStorage]
    Y --> P
```

---

## Diagram 2 — Credit Purchase Flow

```mermaid
flowchart TD
    A([User on Buy Credits Page]) --> B[View Available Packages\nStarter/Growth/Professional/Enterprise]
    B --> C[Select Package]
    C --> D[Select Payment Mode\nDemo: success/fail/pending]
    D --> E[Click Purchase Now]
    E --> F[Generate Idempotency Key\nuuidv4]
    F --> G[Show Confirmation Modal\nPackage + Price + Credits]
    G --> H{User Confirms?}
    H -- No --> B
    H -- Yes --> I[POST /api/credits/purchase\npackage_id + payment_mode + idempotency_key]

    I --> J{Check Idempotency\nKey Exists?}
    J -- Yes --> K[Return Original\nPayment Result]
    K --> L([Show Original Result])

    J -- No --> M{Payment Mode?}

    M -- success --> N[Create Payment Record\nstatus=success]
    N --> O[Add credits + bonus\nto user balance]
    O --> P[Create CreditLedger Entry\nentry_type=purchase]
    P --> Q[Return 200 OK\ncredits_added + new_balance]
    Q --> R[Update UI Balance]
    R --> S[Show Success Toast\nX credits added!]
    S --> T([Redirect to Dashboard])

    M -- fail --> U[Create Payment Record\nstatus=failed]
    U --> V[NO credits added]
    V --> W[Return 200 OK\nstatus=failed, credits_added=0]
    W --> X[Show Failure Toast\nPayment declined]
    X --> B

    M -- pending --> Y[Create Payment Record\nstatus=pending]
    Y --> Z[NO credits added yet]
    Z --> AA[Return 200 OK\nstatus=pending]
    AA --> AB[Show Pending Info\nCredits added after verification]
    AB --> AC{Admin\nReconciles?}
    AC -- No --> AD([Waiting State])
    AC -- Yes --> AE[POST /api/credits/reconcile/id\nAdmin Only]
    AE --> AF[Update Payment status=success]
    AF --> AG[Add Credits to User]
    AG --> AH[Create Ledger Entry]
    AH --> AI([Credits Added])
```

---

## Diagram 3 — Doctor Search & Profile Unlock Flow

```mermaid
flowchart TD
    A([User Navigates to\nFind Doctors Page]) --> B[Load Doctor List\nGET /api/doctors]
    B --> C{Doctors\nFound?}
    C -- No --> D[Show Empty State\nNo results found]
    D --> E[Suggest Filter Changes]
    E --> F[User Modifies Filters]
    F --> B

    C -- Yes --> G[Display Doctor Cards\nName, Specialty, City, Rating\nContact info HIDDEN]
    G --> H[User Applies Filters\nSpecialty/City/Experience/Fee]
    H --> B

    G --> I[User Clicks\nDoctor Card]
    I --> J[Navigate to Doctor Profile Page\nGET /api/doctors/id]
    J --> K{Profile\nPreviously Unlocked?}

    K -- Yes --> L[Show Full Profile\nPhone + Email + Contact\nNo credit charge]

    K -- No --> M[Show Blurred/Hidden\nContact Section\nLock Icon Displayed]
    M --> N[Show Unlock Button\n10 credits required]
    N --> O{User Clicks\nUnlock Profile}

    O -- No --> P([User Browses\nPublic Info Only])

    O -- Yes --> Q[POST /api/credits/unlock\ndoctor_id]
    Q --> R{Check Credit\nBalance >= 10?}

    R -- No --> S[Return 402\nInsufficient Credits]
    S --> T[Show Error\nInsufficient Credits]
    T --> U[Show Buy Credits CTA]
    U --> V([User Goes to\nBuy Credits Page])

    R -- Yes --> W{Already\nUnlocked?}
    W -- Yes --> X[Return Success\nalready_unlocked=true\ncredits_spent=0]
    X --> Y[Reveal Contact Info]

    W -- No --> Z[Deduct 10 Credits\nfrom Balance]
    Z --> AA[Create CreditLedger Entry\nentry_type=unlock]
    AA --> AB[Create DoctorUnlock Record]
    AB --> AC[Return Success\ncredits_spent=10\nnew_balance=X]
    AC --> AD[Update Balance in UI]
    AD --> Y
    Y --> AE([User Sees Full Profile\nName, Phone, Email,\nHospital, Consultation Fee])
```

---

## Diagram Summary

| Diagram | Key Decision Points | Business Rules Covered |
|---------|--------------------|-----------------------|
| Registration & Login | Email uniqueness, password validation, JWT expiry | BR-001 |
| Credit Purchase | Idempotency, payment modes (SC-002, SC-003, SC-005) | BR-007, BR-008, BR-009, BR-010 |
| Doctor Search & Unlock | Empty results (SC-004), insufficient credits (SC-001) | BR-003, BR-004, BR-005, BR-006, BR-011, BR-012 |

---

*Document End — Doctor Data Platform Workflow Diagrams v1.0*
