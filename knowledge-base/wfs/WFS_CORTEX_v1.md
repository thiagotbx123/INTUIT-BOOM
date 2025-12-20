# WFS_CORTEX_v1

Created_at: 2025 12 19
Timezone: America Sao Paulo

## 0 Quick start
Use it as the source of truth for context, scope, data rules, and open questions.

## 1 Purpose and boundaries

### 1.1 What this cortex is
- A compact but detailed memory pack for the Intuit Workforce Solutions project (WFS).
- Optimized for an AI assistant to answer questions, draft messages, and design data and demo plans.

### 1.2 What this cortex is not
- Not a contract or final SOW.
- Not a replacement for Intuit PRDs or official roadmap.
- Not a place to store real customer data or real employee PII.

### 1.3 Project boundary
- WFS is a QuickBooks branded workforce and HCM offering powered by GoCo capabilities plus QuickBooks Payroll.
- WFS work is separate from the Intuit IES demo environments.

## 2 Claude operating rules

### 2.1 Behavior
- Always separate facts, assumptions, and open questions.
- If a detail is missing, propose the minimum reasonable assumption and label it.
- Prefer written clarity over long backstory.
- When drafting Slack or email, keep it short, direct, and action oriented.

### 2.2 Data safety
- Treat all datasets as synthetic unless explicitly labeled as customer provided.
- Never invent real personal identifiers.
- If asked to include PII, mask it by default.

### 2.3 Output modes
- Mode A: Slack update, 3 to 6 bullets, with clear asks and blockers.
- Mode B: SOW or scope text, structured and explicit about assumptions.
- Mode C: Data architecture, tables and fields, deterministic IDs, validation rules.
- Mode D: Demo script, step by step, with preconditions and expected proof points.
- Mode E: Risk register, with impact, likelihood, mitigation, owner, next action.

## 3 What WFS is
- Intuit Workforce Solutions is an HCM platform for small and mid market businesses.
- Combines payroll, HR, benefits, time, and related capabilities.
- Intent: unify employee lifecycle workflows with QuickBooks integration.

## 4 Why TestBox is involved
- WFS sales and enablement need stable, data rich demo environments.
- TestBox provides scenario driven environments with synthetic data.

## 5 Timeline snapshot
- Alpha: December 2025, about 100 customers.
- Beta: February 2026 (some sources say March 2026 - confirm with Intuit)
- GA: May 2026, with May 1, 2026 as key date.

## 6 Key stakeholders

### Intuit WFS team
| Name | Role |
|------|------|
| Ben Hale | Sales enablement |
| Nikki Behn | Marketing lead (GoCo background) |
| Kyla Ellerd | Sales program management |
| Christina Duarte | Leadership, scoping, timeline |
| Nir | Headcount forecast for licensing |
| Kev Lubega | Mineral/WFS integration (key contact for data flow) |

### TestBox team
| Name | Role |
|------|------|
| Katherine Lu | Program lead, SOW drafting |
| Thiago Rodrigues | TSA, data architect, demo reliability |

## 7 Current state (2025-12-19)

### Confirmed
- Demo scope: employee lifecycle (recruiting, onboarding, benefits, payroll)
- Job costing is key differentiator
- TestBox needs technical PRDs for detailed scope
- **GoQuick Alpha Retail** available (Realm ID: 9341455848423964) - EXPLORATION ONLY
- **47 QBO routes mapped** and 100% functional
- **27 WFS reports identified** with direct URLs
- **Mineral HR access confirmed** via SSO (PR_ELITE plan)
- **Intuit Intelligence (AI)** discovered in BETA
- **54+ screenshots captured** of QBO + Mineral

### Blockers
- Missing technical PRDs for prioritized demo stories
- Click path for reps not defined (pending Kev response)
- Final demo environment TBD (GoQuick is temporary)
- Data flow WFS -> Mineral not documented
- User license count needed for February (60 additional in PO)

### Next steps
- Finalize SOW draft with Mineral scope
- Analyze Winter Release doc (24 features, Early Access Feb 4)
- Follow-up with Kev about click path
- Confirm final demo environment with Christina

### Session Consolidation
See: `WFS_SESSION_CONSOLIDATION_20251219.md` for full session details

## 8 Demo Modules

| Module | Purpose | Key Objects |
|--------|---------|-------------|
| Identity/RBAC | Role experiences, safe data access | users, roles, permissions |
| Worker profile | Single source of truth | employee, compensation, tax forms |
| Org chart | Reporting structure visibility | departments, teams, managers |
| Recruiting | Hiring manager pipeline | requisitions, candidates, offers |
| Onboarding | Hire to payroll workflow | templates, tasks, forms |
| Magic Docs | AI document generation | templates, smart fields, e-sign |
| Time off/PTO | Time off management | policies, balances, requests |
| Time/Attendance | Time capture, scheduling | timesheets, schedules |
| Payroll/Benefits | Pay run, benefits enrollment | pay groups, deductions |
| Performance | Performance to compensation | reviews, goals, ratings |
| Workflows | HR process automation | triggers, tasks, approvals |
| Offboarding | Termination workflow | termination, final pay |

## 9 Prioritized Demo Stories

### Story A: Unified PTO
- User flow: employee > manager > payroll admin
- Steps: submit request > approve > balance updates > payroll reflects
- Data: 3 PTO policies, 5-10 pending requests

### Story B: Magic Docs
- User: HR admin
- Steps: generate template > smart fields > e-signature > auto-save
- Data: complete profiles, doc templates

### Story C: Hire to fire lifecycle
- Flow: Recruiting > onboarding > benefits > payroll
- Differentiators: unlimited templates, job costing

### Story D: Job costing
- Confirm where it exists today
- Proof point: labor cost attributed to project/job code

## 10 Golden Thread Data Architecture

### Definition
One employee record flows through multiple modules with consistent IDs.

### Baseline dataset
- Employees: 50 core + future hires pool
- Departments: 6-10
- Locations: 3-6 (multi-state)
- Managers: 8+
- PTO policies: 3
- Pending PTO requests: 5-10
- Doc templates: 5-10
- Workflows: 2 prebuilt
- Recruiting: 5 open reqs, 30 candidates
- Payroll: 2 pay groups, 2 historical runs

### Data freshness
- Weekly: 1-2 new hires, move 1 candidate to hired
- Pay period: run PTO accrual simulation
- Monthly: refresh announcements, reviews

## 11 Delivery Waves

| Wave | Focus | Deliverables |
|------|-------|--------------|
| 0 | Scoping | Collect PRDs, confirm access, licenses |
| 1 | Alpha | Minimum stories, baseline data, enablement guide |
| 2 | Beta | Performance, workflows, richer data |
| 3 | GA | Reliability, monitoring, automation |

## 12 Health Checks

### Daily
- Login as admin, manager, employee
- Worker profile loads
- PTO request works
- Magic Doc template exists

### Weekly
- Payroll linkage works
- Job costing proof point works
- No permission regressions

## 13 Templates

### Slack Update
WFS
- Focus:
- Done:
- Next:
- Blockers:
- Asks:

### Ticket
- Title:
- Context:
- Environment:
- Role used:
- Steps to reproduce:
- Expected vs Actual:
- Impact:
- Owner:
- Priority:

## 14 Machine Index

| Key | Value |
|-----|-------|
| project | Intuit Workforce Solutions (WFS) |
| customer | Intuit |
| timeline.alpha | 2025-12 |
| timeline.beta | 2026-02-04 (Early Access) |
| timeline.ga | 2026-05-01 |
| top_stories | Unified PTO, Magic Docs, Job Costing, Hire to Fire |
| stakeholders.intuit | Ben Hale, Nikki Behn, Kyla Ellerd, Christina Duarte, Nir, Kev Lubega |
| stakeholders.testbox | Katherine Lu, Thiago Rodrigues, Waki |
| blockers | PRDs, Click path, Final environment, Mineral data flow |
| env.exploration | GoQuick Alpha Retail (9341455848423964) |
| env.mineral | apps.trustmineral.com (SSO via QBO) |
| exploration.qbo_routes | 47 |
| exploration.wfs_reports | 27 |
| exploration.screenshots | 54+ |
| exploration.status | COMPLETE |
| winter_release.features | 24 |
| winter_release.early_access | 2026-02-04 |

## 15 Related Documents

| Document | Path |
|----------|------|
| Exploration Complete | WFS_EXPLORATION_COMPLETE.md |
| Slack Intelligence | WFS_SLACK_INTELLIGENCE.md |
| Strategic Insights | WFS_STRATEGIC_INSIGHTS.md |
| Session Consolidation | WFS_SESSION_CONSOLIDATION_20251219.md |
| Project Plan Excel | WFS_PROJECT_PLAN_COMPLETE.xlsx |
| Navigation Map | WFS_NAVIGATION_MAP.md |
| Alpha Retail Map | WFS_ALPHA_RETAIL_MAP.md |
| Mineral HR Map | WFS_MINERAL_HR_MAP.md |
