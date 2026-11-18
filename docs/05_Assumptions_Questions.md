# Assumptions & Client Questions
## Doctor Data Platform — Multiplier AI Assessment (Task 5)

**Document Version:** 1.0  
**Date:** November 2026  

---

## Section A — Assumptions

The following assumptions were made during requirements analysis and system design. These should be validated with the client before final delivery.

| ID | Category | Assumption | Impact if Wrong |
|----|----------|-----------|-----------------|
| ASSUMP-001 | Business Model | The credit-based model is the sole monetization strategy; no subscription tiers exist | Requires additional pricing tier architecture |
| ASSUMP-002 | Credits | 10 credits per profile unlock is a fixed price, not configurable per specialty or tier | Need per-specialty pricing matrix |
| ASSUMP-003 | Credits | Credits do not expire; they remain in the user's wallet indefinitely | Need expiry logic and user communication |
| ASSUMP-004 | Credits | Credits are non-transferable between user accounts | Need transfer workflow |
| ASSUMP-005 | Payments | All payments are simulated ("demo mode") for this assessment; no real payment gateway integration | Real gateway (Razorpay/Stripe) needed for production |
| ASSUMP-006 | Doctor Data | All doctor data is fictional and for demonstration only; no real doctor consent or verification processes exist | Requires DPDP Act / HIPAA compliance and data sourcing |
| ASSUMP-007 | Doctor Data | Doctor profiles are pre-seeded by admins, not self-registered by doctors | Requires doctor onboarding and verification flow if self-registration is needed |
| ASSUMP-008 | Search | The platform serves B2C users (individuals searching for doctors) rather than B2B (hospitals/recruiters) | B2B needs bulk search, CSV export, team accounts |
| ASSUMP-009 | Authentication | Email + password authentication is sufficient; no OTP or social login required | Need OAuth2/Google login or mobile OTP |
| ASSUMP-010 | Roles | Only two roles exist: regular user and admin; no "doctor" role for profile management | Doctor-managed profiles need a third role |
| ASSUMP-011 | Storage | SQLite is acceptable for the demo; production would use PostgreSQL | Schema should remain compatible during migration |
| ASSUMP-012 | Infrastructure | The platform is a single-region deployment; no multi-region failover required | CDN and geo-routing needed if multi-region |
| ASSUMP-013 | Compliance | No KYC or identity verification is required for user registration | Telemedicine regulations may require KYC |
| ASSUMP-014 | Concurrency | The system handles up to 1,000 concurrent users; no horizontal scaling needed immediately | Load balancer and auto-scaling needed at higher volumes |
| ASSUMP-015 | Notifications | No email or SMS notifications are needed; all feedback is in-app | Integration with Sendgrid/Twilio required if notifications needed |
| ASSUMP-016 | Doctor Availability | Doctor availability/appointment booking is out of scope | Appointment module is a separate workstream |
| ASSUMP-017 | Search Algorithm | Simple keyword + filter matching is sufficient; no ML-based ranking or recommendation engine | Elasticsearch or recommendation model needed for advanced discovery |

---

## Section B — Client Questions

The following questions should be answered by the client/product owner before development proceeds to production. They are grouped by domain.

---

### Business Model & Credits

| ID | Question | Why It Matters |
|----|----------|----------------|
| Q-001 | What is the rationale for 10 credits per profile unlock — is this price tested with users? | Affects conversion rate and pricing strategy |
| Q-002 | Should credits expire after a set period (e.g., 12 months)? | Major backend logic change; affects user communication strategy |
| Q-003 | Will you offer a free credits trial for new registrations (e.g., 5 free credits on signup)? | Changes onboarding funnel and acquisition cost model |
| Q-004 | Do you plan to introduce subscription plans alongside credits in the future? | Architecture must accommodate dual pricing models |
| Q-005 | Is there a bulk discount or enterprise pricing for high-volume users (e.g., hospitals buying 10,000+ credits)? | Requires separate package type and billing |

---

### Doctor Data & Profiles

| ID | Question | Why It Matters |
|----|----------|----------------|
| Q-006 | Who is responsible for sourcing, verifying, and updating doctor data? Is there a dedicated data team? | Determines admin tooling needed; affects data quality SLA |
| Q-007 | Will doctors be able to self-register and manage their own profiles? | Requires a "Doctor" portal with verification workflow |
| Q-008 | What verification process exists to confirm a doctor's credentials (MCI registration, degrees)? | Critical for trust and legal compliance |
| Q-009 | Are there geographic restrictions on which doctors can be listed (India only, specific states)? | Affects data seeding strategy and search filters |
| Q-010 | How frequently is doctor data expected to change (contact info, hospital affiliation)? | Determines cache strategy and update notification mechanism |

---

### Payments & Financial

| ID | Question | Why It Matters |
|----|----------|----------------|
| Q-011 | Which payment gateway will be used in production (Razorpay, Stripe, PayU, Cashfree)? | Each has different SDK integration and webhook handling |
| Q-012 | How should failed/pending payment reconciliation be handled — automated polling or manual admin action? | Determines if a cron job or webhook handler is needed |
| Q-013 | Is GST applicable on credit purchases? If so, should invoices be auto-generated? | Requires tax calculation module and invoice PDF generation |
| Q-014 | What is the refund policy for unused credits if a user wants to close their account? | Requires refund workflow and accounting integration |
| Q-015 | Should users be able to request a credit refund if they accidentally unlock the wrong profile? | Needs an appeals process and admin override capability |

---

### Users & Access

| ID | Question | Why It Matters |
|----|----------|----------------|
| Q-016 | What PII (Personally Identifiable Information) is collected and how is it stored under DPDP Act 2023? | May require consent management, data retention policies, and right-to-erasure |
| Q-017 | Should users be able to export their transaction history as PDF or CSV? | Requires report generation service |
| Q-018 | Will the platform support team/organization accounts where credits are shared across multiple users? | Requires team management, shared wallet, and admin hierarchy |

---

### Technical & Infrastructure

| ID | Question | Why It Matters |
|----|----------|----------------|
| Q-019 | What are the expected peak concurrent users and monthly active users (MAU) in year 1? | Critical for infrastructure sizing, database choice, caching strategy |
| Q-020 | Is there an existing authentication system or SSO (SAML/OAuth) to integrate with? | Could replace custom JWT auth entirely |

---

## Section C — Risk Register (from Assumptions)

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R-001 | Credits pricing (10/profile) is too high and reduces adoption | Medium | High | A/B test pricing; introduce first-unlock-free campaign |
| R-002 | Doctor data accuracy issues damage platform trust | High | High | Manual verification process + user reporting mechanism |
| R-003 | DPDP Act non-compliance due to PII storage | Medium | Critical | Engage legal counsel; implement consent management |
| R-004 | Payment gateway integration delays | Medium | High | Build with abstraction layer; prototype with Razorpay first |
| R-005 | SQLite not performant at scale | Low | Medium | Plan PostgreSQL migration before launch |

---

*Document End — Doctor Data Platform Assumptions & Client Questions v1.0*
