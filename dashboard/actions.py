"""Actions: login test, TOTP generation, sweep prompt, retool sync."""

import subprocess
import time
from pathlib import Path

import pyotp

from models import Account

BASE_DIR = Path(__file__).resolve().parent.parent


def test_login(account: Account) -> dict:
    """Generate TOTP code and login info for an account."""
    totp = pyotp.TOTP(account.totp_secret)
    code = totp.now()
    remaining = int(totp.interval - (time.time() % totp.interval))
    return {
        "email": account.email,
        "password": account.password,
        "totp_code": code,
        "totp_remaining_seconds": remaining,
        "login_url": "https://accounts.intuit.com/app/sign-in",
        "entities": len(account.companies),
        "mfa_type": account.mfa_type,
    }


def generate_sweep_prompt(account: Account) -> str:
    """Generate a copiable sweep prompt for Claude Code."""
    return f"QBO Sweep no {account.label} \u2014 {account.email}"


def _file_age_str(path: Path) -> str:
    """Human-readable age of a file (e.g. '2 hours ago', '3 days ago')."""
    if not path.exists():
        return ""
    age_s = time.time() - path.stat().st_mtime
    if age_s < 3600:
        return f"{int(age_s / 60)} min ago"
    if age_s < 86400:
        return f"{int(age_s / 3600)} hours ago"
    return f"{int(age_s / 86400)} days ago"


def sync_retool() -> dict:
    """Full Retool sync: download CSVs from Retool, crossref, update JSON.

    Steps:
    1. Run retool_download_csvs.py (Playwright: open Retool, clear filters, download)
    2. Run retool_crossref.py --update (compare + write retool_env back to JSON)
    3. Force cache refresh
    """
    import json as json_mod

    dl_script = BASE_DIR / "scripts" / "retool_download_csvs.py"
    xref_script = BASE_DIR / "scripts" / "retool_crossref.py"
    prod_csv = BASE_DIR / "knowledge-base" / "access" / "retool_production_export.csv"
    stg_csv = BASE_DIR / "knowledge-base" / "access" / "retool_staging_export.csv"

    steps_log = []
    download_info = {}
    auth_failed = False

    # --- Step 1: Download CSVs from Retool ---
    if dl_script.exists():
        try:
            steps_log.append("Step 1: Downloading CSVs from Retool...")
            dl_result = subprocess.run(
                ["python", str(dl_script)],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(BASE_DIR),
            )

            if dl_result.returncode != 0:
                dl_error = dl_result.stderr.strip() or dl_result.stdout.strip()
                if "session expired" in dl_error.lower() or "not logged in" in dl_error.lower():
                    auth_failed = True
                    steps_log.append("Retool session expired — using existing CSVs")
                else:
                    steps_log.append(f"Download failed: {dl_error}")
            else:
                # Parse download result
                if "__DOWNLOAD_RESULT_JSON__" in dl_result.stdout:
                    raw = dl_result.stdout.split("__DOWNLOAD_RESULT_JSON__")[1].strip()
                    try:
                        download_info = json_mod.loads(raw)
                    except json_mod.JSONDecodeError:
                        pass
                steps_log.append(dl_result.stdout.strip())
        except subprocess.TimeoutExpired:
            steps_log.append("Download timed out (120s) — using existing CSVs")
        except Exception as e:
            steps_log.append(f"Download error: {e} — using existing CSVs")
    else:
        steps_log.append("Step 1: Download script not found — using existing CSVs")

    # CSV status after download attempt
    csv_status = {
        "prod_exists": prod_csv.exists(),
        "stg_exists": stg_csv.exists(),
        "prod_age": _file_age_str(prod_csv) if prod_csv.exists() else None,
        "stg_age": _file_age_str(stg_csv) if stg_csv.exists() else None,
        "download_info": download_info,
        "auth_failed": auth_failed,
    }

    if not xref_script.exists():
        return {
            **csv_status,
            "output": "\n".join(steps_log),
            "errors": "retool_crossref.py not found",
            "success": False,
            "updated": 0,
            "changes": [],
        }

    if not prod_csv.exists():
        return {
            **csv_status,
            "output": "\n".join(steps_log),
            "errors": "",
            "success": False,
            "updated": 0,
            "changes": [],
            "missing_csv": True,
        }

    # --- Step 2: Cross-reference + update JSON ---
    try:
        steps_log.append("\nStep 2: Cross-referencing and updating retool_env...")
        result = subprocess.run(
            ["python", str(xref_script), "--update"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(BASE_DIR),
        )

        # Parse sync result JSON from script output
        updated = 0
        changes = []
        stdout = result.stdout
        if "__SYNC_RESULT_JSON__" in stdout:
            parts = stdout.split("__SYNC_RESULT_JSON__")
            stdout = parts[0]
            try:
                sync_data = json_mod.loads(parts[1].strip())
                updated = sync_data.get("updated", 0)
                changes = sync_data.get("changes", [])
            except (json_mod.JSONDecodeError, IndexError):
                pass

        steps_log.append(stdout.strip())

        # --- Step 3: Force cache refresh ---
        from data import load_accounts

        load_accounts(force=True)

        return {
            **csv_status,
            "output": "\n".join(steps_log),
            "errors": result.stderr,
            "success": result.returncode == 0,
            "updated": updated,
            "changes": changes,
        }
    except subprocess.TimeoutExpired:
        return {
            **csv_status,
            "output": "\n".join(steps_log),
            "errors": "Crossref timeout (60s)",
            "success": False,
            "updated": 0,
            "changes": [],
        }
    except Exception as e:
        return {
            **csv_status,
            "output": "\n".join(steps_log),
            "errors": str(e),
            "success": False,
            "updated": 0,
            "changes": [],
        }


def get_credentials_text(account: Account) -> str:
    """Format credentials for clipboard copy."""
    totp = pyotp.TOTP(account.totp_secret)
    code = totp.now()
    return f"{account.email}\n{account.password}\n{code}"
