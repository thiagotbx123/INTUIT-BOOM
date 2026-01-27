# Worklog: Keystone Construction Payroll - Employee Duplication Fix

**Date:** 2026-01-27
**Who:** Thiago Rodrigues
**Client:** Intuit (Rachel, David Ball)
**Environment:** Keystone Construction (IES Multi-Entity)
**Status:** RESOLVED
**Time spent:** ~2 hours

---

## What happened

Rachel reported payroll errors in Keystone Construction. When I opened Payroll > Employees, I found a mess - 90 employees showing errors. Turns out many employees were duplicated, some appearing 15+ times.

---

## How I found the problem

### Step 1: Looked at the employee list

Went through the list manually. Immediately saw the pattern - names like "Babar, Varun" showing up over and over.

### Step 2: Found something weird

One duplicate had a corrupted name: "Babar, Varun, Babar, Varun" - like two records got smashed together. That same record had an Intuit test email (@mailinator). Red flag.

### Step 3: Checked our original dataset

Pulled our source file (`table_construction_demo_employees.json`) to compare. We have 45 employees in the original. No duplicates there - dataset is clean.

Important find: **Spencer Hiko and Laura Frank don't exist in our dataset**. They were created outside our normal flow.

### Step 4: Talked to Soranzo

Asked him about how our code handles duplicates. He confirmed: TBX code is correct. When QBO API returns "Another employee already using this name", we skip and continue. So the problem is not on our side.

---

## What caused this

**Best guess:** QBO-side automatic recovery

Here's what probably happened:
1. TBX sent requests to create employees
2. Some requests failed (timeout, network error, whatever)
3. TBX got the error and skipped (correct behavior)
4. But QBO processed the request anyway (some internal retry)
5. Result: employee created even though TBX thought it failed
6. Next run: TBX tries again, more duplicates

**Evidence:**
- Corrupted name "Babar, Varun, Babar, Varun" = two payloads merged
- Test email @mailinator = Intuit internal process leaked into environment
- Spencer Hiko / Laura Frank = created outside TBX, unknown source
- Our code works fine = not our bug

---

## How I fixed it

Only option was manual cleanup. Deleted all duplicates one by one, kept only the original record for each employee.

- Duplicates removed: ~86 records
- Time: ~45 minutes
- Method: 100% manual (click, delete, repeat)

---

## Validation test

After cleanup, ran payroll preview to make sure everything works.

**Results:**
- 4 employees showing (correct for Parent entity)
- Names clean (no corrupted ones)
- Total payroll: $16,433.44
- Hours: 320h
- Status: Ready to submit, no errors

Screenshot saved: `Screenshot 2026-01-27 132319.png`

---

## Key findings

| What I found | What it means |
|--------------|---------------|
| Corrupted name pattern | QBO retry/recovery concatenating data |
| @mailinator email | Intuit test process leaked to environment |
| Spencer Hiko / Laura Frank not in dataset | Created outside TBX - unknown source |
| TBX code works correctly | This is not our bug |

---

## What needs to happen next

**Soranzo:**
- Double check my thinking on root cause
- Do we have logs from employee creation for this environment?
- Worth testing: try to manually create duplicate in QBO to prove it blocks

**Kat:**
- Let Rachel/David know cleanup is done
- Decide if we escalate to Intuit Engineering as QBO anomaly

**Alexandra:**
- Validate this ticket (PLA-3227)
- Add screenshot if needed

---

## Reference info

```
Dataset: table_construction_demo_employees.json
Dataset ID: 2ed5d245-0578-43aa-842b-6e1e28367149
CID Keystone Construction (Par.): 9341454156620895
CID Keystone Terra (Ch.): 9341454156620204
```

---

## Timeline

```
2026-01-27
11:00 - Rachel reports payroll problem
11:15 - Started investigating
11:30 - Found massive duplicates
11:45 - Found corrupted name + test email
12:00 - Checked original dataset
12:15 - Talked to Soranzo about error handling
12:30 - Found Spencer Hiko / Laura Frank not in dataset
12:45 - Started manual cleanup
13:15 - Cleanup done
13:23 - Ran validation test (payroll preview)
13:30 - Posted update to team
14:00 - Finished this worklog
```

---

## Related issues

- PLA-3201 (IC Balance Sheet out of balance) - same environment family
- PLA-3227 (this ticket)

---

**Written by:** Thiago Rodrigues
**Date:** 2026-01-27
