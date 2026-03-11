"""Data loader: reads QBO_CREDENTIALS.json + sweep reports."""

import json
import re
import time
from pathlib import Path

from models import Account, AltCredential, Company, SweepResult

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = BASE_DIR / "knowledge-base" / "access" / "QBO_CREDENTIALS.json"
SWEEP_DIR = BASE_DIR / "knowledge-base" / "sweep-learnings"
WORKSPACE_XLSX = Path.home() / "Downloads" / "Intuit_usersworkspace_march32026.xlsx"

_cache: dict = {"accounts": [], "ts": 0}
CACHE_TTL = 60  # seconds


def _parse_sweep_score(text: str) -> float | None:
    """Extract score from sweep report header (first 20 lines only)."""
    header = "\n".join(text.split("\n")[:20])
    patterns = [
        r"\*\*Overall\s+Score[:\s]*\*?\*?\s*(\d+(?:\.\d+)?)/10",
        r"\*\*Revalidation\s+Score[:\s]*\*?\*?\s*(\d+(?:\.\d+)?)/10",
    ]
    for pat in patterns:
        m = re.search(pat, header, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def _parse_sweep_date(text: str) -> str | None:
    """Extract date from sweep report header."""
    m = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    if m:
        return m.group(1)
    return None


def _parse_p1_findings(text: str) -> list[str]:
    """Extract P1 findings from sweep report."""
    findings = []
    for m in re.finditer(r"(?:^|\n)\s*[-*]\s*\*?\*?P1\*?\*?[:\s]+(.+)", text, re.IGNORECASE):
        findings.append(m.group(1).strip().rstrip("*"))
    # Also look for P1 section headers
    p1_section = re.search(r"##\s*P1[^#]*?\n((?:[-*]\s+.+\n?)+)", text, re.IGNORECASE)
    if p1_section:
        for line in p1_section.group(1).strip().split("\n"):
            line = line.strip().lstrip("-* ").strip()
            if line and line not in findings:
                findings.append(line)
    return findings


def _load_sweep_reports() -> dict[str, SweepResult]:
    """Load and parse all sweep reports, keyed by email."""
    results: dict[str, SweepResult] = {}
    if not SWEEP_DIR.exists():
        return results

    for f in sorted(SWEEP_DIR.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        # Extract email
        email_match = re.search(r"\*\*Account:\*\*\s*(\S+@\S+)", text)
        if not email_match:
            continue
        email = email_match.group(1).strip()
        score = _parse_sweep_score(text)
        date = _parse_sweep_date(text) or ""
        p1s = _parse_p1_findings(text)

        # Keep the latest report per email (sorted by filename)
        existing = results.get(email)
        if existing is None or date >= existing.date:
            results[email] = SweepResult(
                date=date,
                score=score,
                report_file=f.name,
                p1_findings=p1s,
            )
    return results


_access_cache: dict = {"data": {}, "ts": 0}


def _load_workspace_accesses() -> dict[str, int]:
    """Load total accesses per workspace_id from Intuit spreadsheet. Cached."""
    now = time.time()
    if _access_cache["data"] and (now - _access_cache["ts"]) < 3600:
        return _access_cache["data"]

    totals: dict[str, int] = {}
    if not WORKSPACE_XLSX.exists():
        return totals

    try:
        import openpyxl

        wb = openpyxl.load_workbook(str(WORKSPACE_XLSX), data_only=True, read_only=True)
        ws = wb["export"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            ws_id = row[7]  # col H = Workspace Id
            count = row[6]  # col G = Count
            if ws_id and count:
                totals[ws_id] = totals.get(ws_id, 0) + int(count)
        wb.close()
    except Exception:
        pass

    _access_cache["data"] = totals
    _access_cache["ts"] = now
    return totals


def _parse_score_from_json(val: str | None) -> float | None:
    """Parse '7.5/10' → 7.5."""
    if not val:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)/10", str(val))
    return float(m.group(1)) if m else None


def load_accounts(force: bool = False) -> list[Account]:
    """Load all QBO accounts with sweep data. Cached for 60s."""
    now = time.time()
    if not force and _cache["accounts"] and (now - _cache["ts"]) < CACHE_TTL:
        return _cache["accounts"]

    with open(CREDENTIALS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    sweep_reports = _load_sweep_reports()
    workspace_accesses = _load_workspace_accesses()
    accounts: list[Account] = []

    for email, info in data.get("accounts", {}).items():
        companies = [
            Company(
                name=c.get("name", ""),
                cid=c.get("cid", ""),
                type=c.get("type", "unknown"),
                priority=c.get("priority", "P1"),
            )
            for c in info.get("companies", [])
        ]

        # Build sweep result: prefer parsed report, fallback to JSON score
        sweep = sweep_reports.get(email)
        json_score = _parse_score_from_json(info.get("sweep_score"))

        if sweep is None and json_score is not None:
            sweep = SweepResult(date="", score=json_score, report_file="", p1_findings=[])
        elif sweep is not None and json_score is not None:
            # JSON sweep_score is manually curated — takes priority
            sweep.score = json_score
        elif sweep is not None and sweep.score is None:
            pass  # no score from either source

        # Extract P1 findings from notes if sweep has none
        if sweep and not sweep.p1_findings and info.get("notes"):
            notes = info["notes"]
            p1_match = re.search(r"P1[:\s]+(.+?)(?:\.|$)", notes)
            if p1_match:
                sweep.p1_findings = [f.strip() for f in p1_match.group(1).split(",") if f.strip()]

        alt_creds = [
            AltCredential(
                email=ac.get("email", ""),
                password=ac.get("password", ""),
                totp_secret=ac.get("totp_secret", ""),
                label=ac.get("label", ""),
            )
            for ac in info.get("alt_credentials", [])
        ]

        account = Account(
            email=email,
            label=info.get("label", ""),
            shortcode=info.get("shortcode", ""),
            password=info.get("password", ""),
            totp_secret=info.get("totp_secret", ""),
            mfa_type=info.get("mfa_type", "totp"),
            dataset=info.get("dataset", ""),
            retool_env=info.get("retool_env", ""),
            companies=companies,
            alt_credentials=alt_creds,
            workspace_id=info.get("workspace_id", ""),
            workspace_name=info.get("workspace_name", ""),
            dataset_id=info.get("dataset_id", ""),
            total_accesses=workspace_accesses.get(info.get("workspace_id", ""), 0),
            last_login=info.get("last_successful_login"),
            sweep=sweep,
            notes=info.get("notes", ""),
        )
        accounts.append(account)

    # Sort: most accessed workspace first, then by score desc
    accounts.sort(
        key=lambda a: (
            -a.total_accesses,
            0 if a.sweep and a.sweep.score else 1,
            -(a.sweep.score if a.sweep and a.sweep.score else 0),
            a.label,
        )
    )

    _cache["accounts"] = accounts
    _cache["ts"] = now
    return accounts


def get_account(shortcode: str) -> Account | None:
    """Get a single account by shortcode."""
    for a in load_accounts():
        if a.shortcode == shortcode:
            return a
    return None
