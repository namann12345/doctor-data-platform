# Wireframes
## Doctor Data Platform — Multiplier AI Assessment (Task 4)

**Document Version:** 1.0  
**Date:** November 2026  

> These wireframes represent the four core screens of the Doctor Data Platform. Layout is described using ASCII art wireframes with annotations. The actual implementation uses Tailwind CSS with a responsive design system.

---

## Wireframe 1 — Login / Registration Screen

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER WINDOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│          ┌───────────────────────────────────────┐             │
│          │       [D]  Doctor Data Platform        │             │
│          │       Healthcare Professional Discovery │             │
│          └───────────────────────────────────────┘             │
│                                                                 │
│          ┌───────────────────────────────────────┐             │
│          │  ┌──────────────┬──────────────────┐  │             │
│          │  │   LOG IN     │    REGISTER       │  │  ← Tab Nav  │
│          │  └──────────────┴──────────────────┘  │             │
│          │                                        │             │
│          │  Email Address                         │             │
│          │  ┌────────────────────────────────┐   │             │
│          │  │  user@demo.com                 │   │             │
│          │  └────────────────────────────────┘   │             │
│          │                                        │             │
│          │  Password                              │             │
│          │  ┌────────────────────────────────┐   │             │
│          │  │  ••••••••••••••         [👁]   │   │             │
│          │  └────────────────────────────────┘   │             │
│          │                                        │             │
│          │  [        Sign In          ]           │  ← Primary  │
│          │                                        │     Button  │
│          │  ─────────── or ───────────            │             │
│          │                                        │             │
│          │  [👤 Fill Demo Credentials ]           │  ← Demo     │
│          │  [👑 Fill Admin Credentials]           │     Buttons │
│          │                                        │             │
│          │  Forgot password? Click here           │             │
│          └───────────────────────────────────────┘             │
│                                                                 │
│    ┌─────────────────────────────────────────────────────┐     │
│    │  💡 Demo Mode — No real payments. All data fictional │     │
│    └─────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

REGISTER TAB (alternate view):
┌───────────────────────────────────────┐
│  Full Name                            │
│  ┌────────────────────────────────┐   │
│  │  Rahul Sharma                  │   │
│  └────────────────────────────────┘   │
│                                        │
│  Email Address                         │
│  ┌────────────────────────────────┐   │
│  │  rahul@example.com             │   │
│  └────────────────────────────────┘   │
│                                        │
│  Password                Password      │
│  Strength: [████░░] Medium             │
│  ┌─────────────────────────────────┐  │
│  │  ••••••••••              [👁]   │  │
│  └─────────────────────────────────┘  │
│                                        │
│  [        Create Account         ]    │
└───────────────────────────────────────┘
```

**Key UI Elements:**
- Tab switcher: Login / Register
- Email + password fields with show/hide toggle
- Demo credential fill buttons (reduces friction for evaluators)
- Password strength indicator on register
- Toast notifications for errors/success

---

## Wireframe 2 — Dashboard

```
┌────────────────────────────────────────────────────────────────────┐
│  BROWSER WINDOW                                                    │
├─────────────┬──────────────────────────────────────────────────────┤
│  SIDEBAR    │  MAIN CONTENT AREA                                   │
│  ───────    │  ─────────────                                       │
│  [D]        │  Welcome back, Rahul 👋                              │
│  Doctor     │  Here's what's happening with your account           │
│  Data       │                                                       │
│  Platform   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│             │  │💳 Credit │ │📈Credits │ │💰Credits │ │🔓Docs  │ │
│  ─────────  │  │ Balance  │ │Purchased │ │  Used    │ │Unlocked│ │
│  💰 Credits │  │          │ │          │ │          │ │        │ │
│  140 cr     │  │ 140 cr   │ │ 250 cr   │ │ 110 cr   │ │  11    │ │
│  Buy more → │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│             │                                                       │
│  NAV ITEMS  │  QUICK ACTIONS                                        │
│  ─────────  │  ┌──────────────┐ ┌───────────────┐ ┌───────────┐  │
│ 🏠 Dashboard│  │🔍 Find       │ │🛒 Buy Credits │ │📄 Trans-  │  │
│ 🔍 Find Dr. │  │  Doctors     │ │   From ₹99    │ │   actions │  │
│ 💳 Buy Cr.  │  │  Search & ↗ │ │              ↗│ │          ↗│  │
│ 📄 Transact │  └──────────────┘ └───────────────┘ └───────────┘  │
│ 👤 Profile  │                                                       │
│             │  ┌───────────────────────────────┐ ┌─────────────┐  │
│  ─────────  │  │  CREDIT BALANCE HISTORY       │ │RECENT ACT.  │  │
│  Rahul S.   │  │  📈 Line Chart                │ │             │  │
│  rahul@...  │  │                               │ │ +100 cr     │  │
│             │  │   250 ┤        ╭──            │ │  Growth pkg │  │
│             │  │   200 ┤   ╭────╯              │ │  Nov 15     │  │
│             │  │   150 ┤╭──╯                   │ │             │  │
│             │  │   100 ┤╯                      │ │ -10 cr      │  │
│             │  │    Nov 1  Nov 8  Nov 15        │ │  Dr. Unlock │  │
│             │  └───────────────────────────────┘ │  Nov 14     │  │
│             │                                     └─────────────┘  │
└─────────────┴──────────────────────────────────────────────────────┘
```

**Key UI Elements:**
- Sidebar: logo, credit balance widget, navigation, user info
- 4 stats cards: balance, purchased, spent, unlocked count
- 3 quick action cards: Find Doctors, Buy Credits, Transactions
- Credit balance line chart (recharts)
- Recent activity list (last 5 transactions)

---

## Wireframe 3 — Buy Credits Page

```
┌────────────────────────────────────────────────────────────────────┐
│  SIDEBAR   │  Buy Credits                                          │
│            │  Purchase credits to unlock doctor profiles. Each     │
│            │  profile costs 10 credits.                            │
│            │                                                        │
│            │  ┌────────────────────────────────────────────────┐  │
│            │  │ 💳 Current Balance: 140 credits                 │  │
│            │  └────────────────────────────────────────────────┘  │
│            │                                                        │
│            │  ⚠️ Demo Payment System — No real charges made        │
│            │                                                        │
│            │  🛡 DEMO PAYMENT MODE                                 │
│            │  ┌───────────┐ ┌────────────┐ ┌─────────────────┐   │
│            │  │✅ Success  │ │❌ Failed   │ │⏳ Pending        │   │
│            │  │Credits add│ │No credits  │ │Await confirm    │   │
│            │  │immediately│ │(SC-002)    │ │(SC-003)         │   │
│            │  └───────────┘ └────────────┘ └─────────────────┘   │
│            │                                                        │
│            │  CREDIT PACKAGES                                       │
│            │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │
│            │  │ Starter  │ │★ Growth  │ │Profess.  │ │Enterp. │  │
│            │  │          │ │ POPULAR  │ │          │ │        │  │
│            │  │  ₹99     │ │  ₹399   │ │  ₹699   │ │ ₹1499  │  │
│            │  │  50 cr   │ │ 100 cr  │ │ 200 cr  │ │ 500 cr  │  │
│            │  │          │ │ +20 bonus│ │ +50 bonus│ │+150 bon│  │
│            │  │= 50 total│ │= 120 tot│ │= 250 tot│ │= 650 tot│  │
│            │  │₹1.98/cr  │ │₹3.33/cr │ │₹2.80/cr │ │₹2.30/cr│  │
│            │  │[Select]  │ │[Select✓]│ │[Select]  │ │[Select]│  │
│            │  └──────────┘ └──────────┘ └──────────┘ └────────┘  │
│            │                                                        │
│            │  ┌────────────────────────────────────────────────┐  │
│            │  │  Growth Package  · 120 total credits · ₹399   │  │
│            │  │                          [Purchase Now →]       │  │
│            │  └────────────────────────────────────────────────┘  │
│            │                                                        │
│            │  ✅ Payment Successful!                               │
│            │  New balance: 260 credits                             │
└────────────┴───────────────────────────────────────────────────────┘

CONFIRM MODAL (overlay):
┌──────────────────────────────┐
│  Confirm Purchase            │
│  ─────────────────────────── │
│  Package:    Growth           │
│  Credits:    120              │
│  Amount:     ₹399             │
│  Mode:       SUCCESS (Demo)   │
│  ─────────────────────────── │
│  [Cancel]    [Pay ₹399 →]    │
└──────────────────────────────┘
```

**Key UI Elements:**
- Current balance banner
- Demo payment mode selector (3 options with scenario labels)
- 4 package cards with pricing, credits, bonus, per-credit cost
- Featured package badge "Most Popular"
- Confirmation modal before purchase
- Result banner with new balance / failure reason

---

## Wireframe 4 — Doctor Search & Results

```
┌─────────────────────────────────────────────────────────────────────┐
│  SIDEBAR   │  Find Doctors                                          │
│            │  Search from 31+ verified healthcare professionals     │
│            │                                                         │
│            │  FILTERS ROW                                           │
│            │  ┌─────────────┐ ┌───────────┐ ┌──────────────────┐  │
│            │  │🔍 Search    │ │Specialty ▼│ │City ▼            │  │
│            │  │  "cardiolog"│ │Cardiology │ │Mumbai            │  │
│            │  └─────────────┘ └───────────┘ └──────────────────┘  │
│            │  ┌──────────────────────┐ ┌─────────────┐            │
│            │  │Min Exp: ━━●─────── 5+│ │[Clear All]  │            │
│            │  └──────────────────────┘ └─────────────┘            │
│            │                                                         │
│            │  Showing 4 of 31 doctors (Cardiology, Mumbai)         │
│            │                                                         │
│            │  DOCTOR CARDS GRID (3 columns)                         │
│            │  ┌───────────────────┐ ┌───────────────────┐          │
│            │  │  Dr. Arjun Mehta  │ │  Dr. Priya Sharma │          │
│            │  │  Cardiologist     │ │  Cardiologist     │          │
│            │  │  ★★★★★ 4.9       │ │  ★★★★☆ 4.7       │          │
│            │  │  Apollo Mumbai    │ │  Fortis Mumbai    │          │
│            │  │  12 yrs exp       │ │  8 yrs exp        │          │
│            │  │  📍 Mumbai        │ │  📍 Mumbai        │          │
│            │  │  💰 ₹800/consult  │ │  💰 ₹600/consult  │          │
│            │  │  ━━━━━━━━━━━━━━━━ │ │  ━━━━━━━━━━━━━━━━ │          │
│            │  │  📞 •••••••••     │ │  📞 ••••••••• 🔒  │          │
│            │  │  ✉️ •••@••••      │ │  ✉️ ••••@••••     │          │
│            │  │  [View Profile]   │ │  [🔓 Unlock 10cr] │          │
│            │  └───────────────────┘ └───────────────────┘          │
│            │                                                         │
│            │  ┌───────────────────┐ ┌───────────────────┐          │
│            │  │  Dr. Ravi Kumar   │ │  Dr. Sonal Patel  │          │
│            │  │  Cardiologist     │ │  Cardiologist     │          │
│            │  │  ★★★★☆ 4.6       │ │  ★★★★★ 4.8       │          │
│            │  │  ...              │ │  ...              │          │
│            │  │  [🔓 Unlock 10cr] │ │  [🔓 Unlock 10cr] │          │
│            │  └───────────────────┘ └───────────────────┘          │
│            │                                                         │
│            │  ← 1  [2] [3]  →    (Pagination)                      │
└────────────┴────────────────────────────────────────────────────────┘

DOCTOR PROFILE PAGE (after clicking View Profile):
┌──────────────────────────────────────────────────────┐
│  ← Back to Search                                    │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  [DM]  Dr. Arjun Mehta                 ✅Unlocked│ │
│  │        MBBS, MD (Cardiology)                    │ │
│  │        Apollo Hospital, Mumbai                  │ │
│  │        ★★★★★ 4.9 · 234 reviews                 │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  About          Consultation     Contact              │
│  ────────────────────────────────────────────         │
│  12 years exp   ₹800/consult     📞 +91 98765 43210  │
│  Cardiology     Mon-Sat 9-5      ✉️  arjun@apollo.com │
│                                                       │
│  Bio: Dr. Arjun Mehta is a senior cardiologist...    │
│                                                       │
│  [🔒 LOCKED — Unlock for 10 credits]                 │
│  (shown when NOT yet unlocked)                        │
└──────────────────────────────────────────────────────┘
```

**Key UI Elements:**
- Filter bar: text search, specialty dropdown, city dropdown, experience slider
- Result count with active filters
- Doctor card grid: name, specialty, rating, hospital, city, experience, fee
- Contact info blurred/hidden with lock icon until unlocked
- Unlock button showing credit cost
- Pagination controls
- Detailed profile page with full contact info (after unlock)

---

## Design System Reference

| Element | Value |
|---------|-------|
| Primary Color | `#1E3A8A` (blue-900) |
| Background | `#F8FAFC` (slate-50) |
| Card Background | `#FFFFFF` white |
| Border | `#E2E8F0` (slate-200) |
| Success | `#059669` (emerald-600) |
| Error | `#DC2626` (red-600) |
| Warning | `#D97706` (amber-600) |
| Font | Inter (system fallback) |
| Border Radius | `0.75rem` (12px) cards, `0.5rem` buttons |
| Responsive Breakpoints | Mobile < 768px, Tablet 768-1024px, Desktop > 1024px |

---

*Document End — Doctor Data Platform Wireframes v1.0*
