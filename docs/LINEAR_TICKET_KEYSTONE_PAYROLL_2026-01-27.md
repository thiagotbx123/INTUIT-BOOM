# LINEAR TICKET - Para Alexandra Criar

---

## Dados do Ticket

**Title:** [BUG] Keystone Construction - Employee Duplication in Payroll (RESOLVED)

**Project:** Intuit

**Labels/Tags:**
- `bug-investigation`
- `qbo-payroll`
- `keystone-construction`
- `resolved`

**Priority:** High (was urgent, now resolved)

**Assignee:** Thiago Rodrigues (investigator) / Alexandra Lacerda (documentation)

---

## Description

### Summary

Massive employee duplication discovered in Keystone Construction payroll - 90 employees showing errors, with some names appearing 15+ times. Issue was investigated, root cause identified (QBO-side anomaly), and resolved via manual cleanup.

---

### Environment

| Field | Value |
|-------|-------|
| Ambiente | Keystone Construction (IES Multi-Entity) |
| Dataset | `construction_demo` |
| Dataset ID | `2ed5d245-0578-43aa-842b-6e1e28367149` |
| CID Parent | `9341454156620895` |
| CID Terra | `9341454156620204` |

---

### Problem Description

Rachel reported payroll errors in Keystone Construction. Investigation revealed:

1. **90 employees with errors** in the system
2. **Massive duplication** - employees like "Babar, Varun" appearing 15+ times
3. **Corrupted record** found: name "Babar, Varun, Babar, Varun" with Intuit test email (@mailinator)
4. **External employees** - Spencer Hiko and Laura Frank exist in environment but NOT in our original dataset

---

### Root Cause Analysis

**Primary Hypothesis:** QBO-side automatic recovery creating duplicates

**Evidence:**
- Corrupted name suggests payload concatenation from retry/recovery
- Test email (@mailinator) indicates Intuit internal process
- TBX error handling confirmed working correctly (per Soranzo)
- Original dataset is clean (45 unique employees, no duplicates)

**Conclusion:** Problem is NOT in TBX code. QBO may have recovered failed API calls and created duplicate records.

---

### Resolution

**Action taken:** Manual deletion of ~86 duplicate records

**Process:**
1. Identified all duplicates in Payroll > Employees
2. Deleted duplicates one by one
3. Preserved only original/cleanest record for each employee
4. Validated with payroll preview test

**Time to resolve:** ~2 hours (investigation + cleanup)

---

### Validation

Payroll preview test after cleanup:

| Field | Value |
|-------|-------|
| Employees | 4 (unique) |
| Total Hours | 320h |
| Gross Pay | $14,676.91 |
| Total Payroll Cost | $16,433.44 |
| Status | Ready to submit, no errors |

Screenshot attached: `Screenshot 2026-01-27 132319.png`

---

### Key Findings

| Finding | Implication |
|---------|-------------|
| Name corruption pattern | QBO recovery concatenating payloads |
| @mailinator test email | Intuit internal process leaked to environment |
| Spencer Hiko / Laura Frank | Created outside TBX flow - unknown source |
| TBX code OK | Not our bug |

---

### Follow-up Actions

| Action | Owner | Status |
|--------|-------|--------|
| Technical double-check | Soranzo | Pending |
| Client communication | Kat | Pending |
| Consider Intuit Engineering escalation | Kat | Pending |
| Monitor for recurrence | Team | Ongoing |

---

### Documentation

Full worklog: `docs/WORKLOG_KEYSTONE_PAYROLL_DUPLICATION_2026-01-27.md`

---

### Related Issues

- PLA-3201 (IC Balance Sheet out of balance) - same environment family
- Rachel bad data thread 2026-01-26 - same environment

---

## Attachments to Include

1. `Screenshot 2026-01-27 132319.png` - Payroll preview after cleanup
2. `WORKLOG_KEYSTONE_PAYROLL_DUPLICATION_2026-01-27.md` - Full investigation log

---

## Comments to Add

### Comment 1 (Initial)
```
Investigation started after Rachel reported payroll errors. Found massive employee duplication - some names appearing 15+ times. Starting deep dive.
```

### Comment 2 (Discovery)
```
Key finding: corrupted employee name "Babar, Varun, Babar, Varun" with Intuit test email. Also found 2 employees (Spencer Hiko, Laura Frank) that don't exist in our dataset - created externally.
```

### Comment 3 (Root Cause)
```
Confirmed with Soranzo: TBX error handling works correctly. Root cause is likely QBO-side recovery creating duplicates from failed API calls. Not a TBX bug.
```

### Comment 4 (Resolution)
```
Manual cleanup complete. Deleted ~86 duplicate records. Validated with payroll preview - 4 unique employees, calculations correct, ready to submit. Environment operational.
```

---

## Instructions for Alexandra

1. Create new ticket in Linear under Intuit project
2. Copy title exactly as shown above
3. Apply all tags listed
4. Copy description content
5. Attach screenshot file
6. Link to worklog document
7. Add the 4 comments in sequence
8. Link to related issues if they exist in Linear (PLA-3201)
9. Set status to "Done" or "Resolved"

---

**Prepared by:** Thiago Rodrigues
**Date:** 2026-01-27
**For:** Alexandra Lacerda (to create in Linear)
