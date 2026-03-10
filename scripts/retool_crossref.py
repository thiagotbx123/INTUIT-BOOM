#!/usr/bin/env python3
"""Cross-reference Retool exports with QBO_CREDENTIALS.json"""

import argparse
import csv
import json
import os
import sys

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


def update_credentials_from_retool(creds_path, prod_trials, stg_trials):
    """Sync retool_env, password, and TOTP from Retool CSVs into QBO_CREDENTIALS.json.

    Updates:
    - retool_env: production / staging / NOT_IN_RETOOL
    - password: if Retool has a different one
    - totp_secret: if Retool has a different one (old value saved as totp_secret_alt)

    Returns (changed_count, changes_list).
    """
    with open(creds_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = 0
    changes = []
    prod_emails = set(prod_trials.keys())
    stg_emails = set(stg_trials.keys())

    for email, acct in data["accounts"].items():
        # --- retool_env ---
        if email in prod_emails:
            new_env = "production"
        elif email in stg_emails:
            new_env = "staging"
        else:
            new_env = "NOT_IN_RETOOL"

        old_env = acct.get("retool_env", "")
        if old_env != new_env:
            acct["retool_env"] = new_env
            changed += 1
            changes.append({"email": email, "field": "retool_env", "old": old_env, "new": new_env})

        # --- password & totp: sync from Retool (prod takes priority over staging) ---
        retool_data = prod_trials.get(email) or stg_trials.get(email)
        if not retool_data:
            continue

        # Password
        rt_pw = retool_data.get("password")
        local_pw = acct.get("password")
        if rt_pw and local_pw and rt_pw != local_pw:
            acct["password"] = rt_pw
            changed += 1
            changes.append({"email": email, "field": "password", "old": "***", "new": "synced from Retool"})

        # TOTP
        rt_totp = retool_data.get("totp_token")
        local_totp = acct.get("totp_secret")
        if rt_totp and local_totp and rt_totp != local_totp:
            # Check if it matches the alt key (rotation scenario)
            alt = acct.get("totp_secret_alt")
            if alt == rt_totp:
                continue  # Already tracked as alt, no change needed
            # Save old as alt, update main
            acct["totp_secret_alt"] = local_totp
            acct["totp_secret"] = rt_totp
            changed += 1
            changes.append({"email": email, "field": "totp_secret", "old": "***", "new": "synced from Retool"})

    if changed > 0:
        with open(creds_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return changed, changes


def main():
    parser = argparse.ArgumentParser(description="Cross-reference Retool exports with QBO_CREDENTIALS.json")
    parser.add_argument("--update", action="store_true", help="Write retool_env back to QBO_CREDENTIALS.json")
    args = parser.parse_args()

    creds_path = os.path.join(BASE, "knowledge-base/access/QBO_CREDENTIALS.json")
    prod_csv = os.path.join(BASE, "knowledge-base/access/retool_production_export.csv")
    stg_csv = os.path.join(BASE, "knowledge-base/access/retool_staging_export.csv")

    if not os.path.exists(prod_csv):
        print("ERROR: Production CSV not found at:", prod_csv, file=sys.stderr)
        sys.exit(1)

    # Parse
    prod = parse_retool_csv(prod_csv)
    stg = parse_retool_csv(stg_csv) if os.path.exists(stg_csv) else {}

    with open(creds_path, "r", encoding="utf-8") as f:
        creds = json.load(f)
    existing = set(creds["accounts"].keys())

    print("=" * 80)
    print("RETOOL x QBO_CREDENTIALS CROSS-REFERENCE")
    print("=" * 80)

    print(f"\n  Production CSV: {len(prod)} trials")
    print(f"  Staging CSV:    {len(stg)} trials")
    print(f"  Local creds:    {len(existing)} accounts")

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

    # Write-back if --update flag is set
    if args.update:
        print("\n=== SYNCING FROM RETOOL -> QBO_CREDENTIALS.json ===")
        changed, changes = update_credentials_from_retool(creds_path, prod, stg)
        if changed:
            for c in changes:
                print(f"  {c['email']}: {c['field']} {c['old']!r} -> {c['new']!r}")
            print(f"\n  SYNCED: {changed} change(s)")
        else:
            print("  No changes needed — all credentials already in sync")
        # Output JSON summary for dashboard consumption
        print("\n__SYNC_RESULT_JSON__")
        print(json.dumps({"updated": changed, "changes": changes}))


if __name__ == "__main__":
    main()
