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


def sync_retool() -> dict:
    """Run retool_crossref.py and return output."""
    script = BASE_DIR / "scripts" / "retool_crossref.py"
    if not script.exists():
        return {"output": "", "errors": "retool_crossref.py not found", "success": False}
    try:
        result = subprocess.run(
            ["python", str(script)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(BASE_DIR),
        )
        return {
            "output": result.stdout,
            "errors": result.stderr,
            "success": result.returncode == 0,
            "filter_cleared": True,
            "filter_note": "Before downloading CSVs from Retool, always click the Filter icon on the left sidebar and 'Clear All Filters' to ensure you get the full unfiltered dataset.",
        }
    except subprocess.TimeoutExpired:
        return {"output": "", "errors": "Timeout (60s)", "success": False, "filter_cleared": False, "filter_note": ""}
    except Exception as e:
        return {"output": "", "errors": str(e), "success": False, "filter_cleared": False, "filter_note": ""}


def get_credentials_text(account: Account) -> str:
    """Format credentials for clipboard copy."""
    totp = pyotp.TOTP(account.totp_secret)
    code = totp.now()
    return f"{account.email}\n{account.password}\n{code}"
