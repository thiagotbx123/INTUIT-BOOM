# Intuit Ecosystem Intelligence — 2026-04-13
**Source:** Slack search (8 queries), KB audit, Downloads scan
**Period covered:** Apr 1–13, 2026

---

## 1. ORGANIZATIONAL CHANGES (HIGH IMPACT)

| Person | New Role | Impact |
|--------|----------|--------|
| Thiago Rodrigues | Senior TSA | Owns Intuit (largest customer), driving ops improvements |
| Katherine (Kat) Lu | Head of Customer | Owns post-contract end-to-end (deploy, CS, engagement, expansion) |
| Waki (Wakigawa) | Office of the CEO | MONARCH + strategic w/ Sam |
| Yasmim | Assoc. Data Engineer | QA → data quality transition |
| Augusto | Software Engineer | Recognized as "recent Intuit owner on Platypus" |

**Structural:**
- Kat's scope: GTM, TSAs, CE team all through her
- Data Generator Pod: Thais + Yasmim + Evelyn
- Implementation Captains: prevent Gabriel bottleneck

---

## 2. SPRING RELEASE 2026

- **Effort Tracker v1** built by Alexandra
- **Apr 17 deadline**: Intuit must finalize scope ("Write and Straight" doc)
- Click paths NOT yet shared by Intuit (Alexandra using assumptions)
- Open: Should TestBox prepare "New Data Needed" or Intuit provides?
- May release plan drafted by Gayathri (heavy DRAFT caveat)
- Intuit release meeting: 9 AM Apr 13

---

## 3. WFS IMPLEMENTATION

- **Phase**: M1 Foundation & Alignment
- **Discovery**: Two backends — Payroll API + GoCo HR API
- **Stories**: 6 demo stories available
- **Target**: SHRM conference June 2026
- **Blocker**: PLA-3431 (Construction Payroll history not found — waiting Soranzo)
- Mineral HR discovery session scheduled
- Weekly sync started with all teams

---

## 4. ENVIRONMENT HEALTH

- Weekly health reports ~50% accurate on P&L errors
- Skipped activities don't filter by date (2025 noise)
- Sam saw channel without context; Kat clarified "still calibrating"
- QBOA MM environment: login issue resolved (uses Construction dataset/Keystone)

---

## 5. DATASET & INGESTION

- **V2 migration**: PLA-3376 complete, Postgres V2 on Fly.io
- **Cash Flow Fix (PLA-3416)**: 93 invoices inserted, Augusto confused about gate 2
- **V2 Credentials**: Thiago got from Lucas Scheffel (Apr 13), not yet in Bitwarden broadly

---

## 6. NEW BUSINESS

### Nooks (Pre-Sales)
- Email engagement metrics at scale
- Internal APIs for bulk call ingest (power dialer)
- Timeline: mid-April
- Comparable: Apollo, Outreach, Gong
- Kat wants time-boxed; Thiago suggested Gabi with "smart scope"

### Diocese Non-Profit
- **CANCELLED** — Intuit decided not to pursue

### Accountant Suite
- Preliminary assessment delivered, BETA account created
- Approach as new project, scope from scratch
- Priority P2

---

## 7. MONARCH

- First TSA workflow tests/executions by next Thursday
- Gabi + Carlos fully onboarded
- MON-74: Autonomous POC Generation Service spike
- Role-based access: TSAs, pre-sales, CEs each get own pipeline views

---

## 8. ACTIVE BLOCKERS

| Ticket | Description | Owner | Status |
|--------|-------------|-------|--------|
| PLA-3431 | Construction Payroll history not found | Augusto | Blocked (Soranzo) |
| PLA-3416 | Cash flow invoices gate 2 | Augusto | Confusion |
| — | Spring Release scope not locked | Intuit | Apr 17 deadline |
| — | Health check ~50% P&L accuracy | Augusto | Calibrating |
| — | QSP 2FA blocked | — | No fix path |
| — | Product Events $0 revenue | — | Structural |

---

*Generated: 2026-04-13 by deep refresh (Slack + KB + Downloads + QBO_DEMO_MANAGER)*
