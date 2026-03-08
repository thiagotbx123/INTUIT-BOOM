#!/usr/bin/env python3
"""Cross-reference Retool exports with QBO_CREDENTIALS.json"""

import csv
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_retool_csv(path):
    trials = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row["Email"]
            ctx = json.loads(row["Context"])
            auth = ctx.get("admin_authentication", {})
            user = auth.get("user", {})
            extras = auth.get("extras", {})
            companies = extras.get("companies", [])
            trials[email] = {
                "email": email,
                "password": user.get("password"),
                "totp_token": user.get("totp_token"),
                "state": row["State"],
                "dataset": extras.get("dataset"),
                "environment": extras.get("environment"),
                "companies": companies,
                "created_at": row["Created at"],
                "last_run_at": row.get("Last run at", ""),
            }
    return trials


# Parse
prod = parse_retool_csv(os.path.join(BASE, "knowledge-base/access/retool_production_export.csv"))
stg = parse_retool_csv(os.path.join(BASE, "knowledge-base/access/retool_staging_export.csv"))

with open(os.path.join(BASE, "knowledge-base/access/QBO_CREDENTIALS.json"), "r", encoding="utf-8") as f:
    creds = json.load(f)
existing = set(creds["accounts"].keys())

print("=" * 80)
print("RETOOL x QBO_CREDENTIALS CROSS-REFERENCE")
print("=" * 80)

print("\n=== PRODUCTION TRIALS ===")
for email, t in sorted(prod.items(), key=lambda x: x[1].get("created_at", ""), reverse=True):
    tag = "YES" if email in existing else "NEW"
    ds = t.get("dataset") or "N/A"
    cos = len(t.get("companies", []))
    state = t["state"] or "N/A"
    print(f"  [{tag:>3}] {email:<55} ds={ds:<22} {cos}co  state={state}")

print("\n=== CREDENTIAL DISCREPANCIES ===")
found = False
for email, t in prod.items():
    if email not in existing:
        continue
    acct = creds["accounts"][email]

    # TOTP check
    rt = t.get("totp_token")
    lt = acct.get("totp_secret")
    if rt and lt and rt != lt:
        alt = acct.get("totp_secret_alt") or acct.get("totp_secret_old")
        print(f"  TOTP DIFF: {email}")
        print(f"    Retool: {rt}")
        print(f"    Local:  {lt}")
        if alt:
            print(f"    Alt:    {alt} {'(MATCHES!)' if alt == rt else '(no match)'}")
        found = True

    # Password check
    rp = t.get("password")
    lp = acct.get("password")
    if rp and lp and rp != lp:
        print(f"  PASSWORD DIFF: {email}")
        print(f"    Retool: {rp}")
        print(f"    Local:  {lp}")
        found = True

    # Company count
    rc = len(t.get("companies", []))
    lc = len(acct.get("companies", []))
    if rc != lc:
        print(f"  COMPANY COUNT DIFF: {email} (Retool={rc} vs Local={lc})")
        found = True

if not found:
    print("  No discrepancies found!")

print("\n=== NEW ACCOUNTS (Retool Prod, NOT in local creds) ===")
new_found = False
for email, t in prod.items():
    if email not in existing:
        cids = [c["id"] for c in t.get("companies", [])]
        ps = [c.get("parent_status", "?") for c in t.get("companies", [])]
        print(f"  {email}")
        print(f"    Password: {t['password']}")
        print(f"    TOTP:     {t['totp_token']}")
        print(f"    Dataset:  {t.get('dataset', '?')}")
        print(f"    CIDs:     {list(zip(cids, ps))}")
        print()
        new_found = True
if not new_found:
    print("  None - all Retool accounts already in local creds")

print("\n=== LOCAL ACCOUNTS NOT IN RETOOL PRODUCTION ===")
orphan_found = False
for email in sorted(existing):
    if email not in prod:
        acct = creds["accounts"][email]
        label = acct.get("label", "?")
        print(f"  {email} ({label})")
        orphan_found = True
if not orphan_found:
    print("  None - all local accounts exist in Retool")

# CID comparison for matching accounts
print("\n=== CID INVENTORY (Retool Production) ===")
total_cids = 0
for email, t in sorted(prod.items()):
    cos = t.get("companies", [])
    if cos:
        total_cids += len(cos)
        parents = [c["id"] for c in cos if c.get("parent_status") == "parent"]
        children = [c["id"] for c in cos if c.get("parent_status") == "child"]
        ds = t.get("dataset", "?")
        print(f"  {email} [{ds}]")
        if parents:
            print(f"    Parents:  {parents}")
        if children:
            print(f"    Children: {children}")

print(f"\n  TOTAL: {len(prod)} accounts, {total_cids} company IDs")

# Staging unique accounts
print("\n=== STAGING-ONLY ACCOUNTS (not in Production) ===")
stg_only = set(stg.keys()) - set(prod.keys())
for email in sorted(stg_only):
    t = stg[email]
    ds = t.get("dataset") or "N/A"
    cos = len(t.get("companies", []))
    print(f"  {email} ds={ds} {cos}co")
