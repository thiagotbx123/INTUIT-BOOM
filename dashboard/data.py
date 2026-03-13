"""Data loader: reads QBO_CREDENTIALS.json + sweep reports."""

import json
import re
import time
from pathlib import Path

from models import Account, AltCredential, Company, SweepHistoryEntry, SweepResult

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = BASE_DIR / "knowledge-base" / "access" / "QBO_CREDENTIALS.json"
SWEEP_DIR = BASE_DIR / "knowledge-base" / "sweep-learnings"
WORKSPACE_XLSX = Path.home() / "Downloads" / "Intuit_usersworkspace_march32026.xlsx"

_cache: dict = {"accounts": [], "ts": 0}
CACHE_TTL = 60  # seconds
CONFIGS_DIR = Path(__file__).resolve().parent / "configs"

# Finding actions registry (lazy-loaded)
_finding_actions: list[dict] | None = None


def _load_finding_actions() -> list[dict]:
    """Load finding action patterns from config."""
    global _finding_actions
    if _finding_actions is None:
        path = CONFIGS_DIR / "finding_actions.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            _finding_actions = data.get("actions", [])
        else:
            _finding_actions = []
    return _finding_actions


def classify_finding(text: str) -> dict:
    """Enrich a finding string with action metadata from the registry.

    Returns dict with: text, owner, action, blocker, when.
    owner: auto | manual | platform | none
    when: immediate | next_sweep | backlog | never
    """
    result = {"text": text, "owner": "", "action": "", "blocker": "", "when": ""}
    for entry in _load_finding_actions():
        if re.search(entry["pattern"], text, re.IGNORECASE):
            result["owner"] = entry.get("owner", "")
            result["action"] = entry.get("action", "")
            result["blocker"] = entry.get("blocker", "")
            result["when"] = entry.get("when", "")
            break
    return result


def _parse_sweep_score(text: str) -> float | None:
    """Extract score from sweep report (header first, then full text tables)."""
    header = "\n".join(text.split("\n")[:30])
    patterns = [
        r"\*\*Overall\s+Score[:\s]*\*?\*?\s*(\d+(?:\.\d+)?)/10(?!\d)",
        r"\*\*Revalidation\s+Score[:\s]*\*?\*?\s*(\d+(?:\.\d+)?)/10(?!\d)",
    ]
    for pat in patterns:
        m = re.search(pat, header, re.IGNORECASE)
        if m:
            return float(m.group(1))
    # Fallback: table format "| Realism Score | **6.3/10** |"
    m = re.search(r"\|\s*Realism\s+Score\s*\|\s*\*?\*?(\d+(?:\.\d+)?)/10(?!\d)", text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    return None


def _parse_sweep_date(text: str) -> str | None:
    """Extract date from sweep report header."""
    m = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    if m:
        return m.group(1)
    return None


def _parse_realism_score(text: str) -> int | None:
    """Extract realism score (0-100) from report."""
    patterns = [
        r"\*\*(?:Overall\s+)?Realism(?:\s+Score)?[:\s]*\*?\*?\s*(\d+)/100",
        r"Overall\s+Realism[:\s]*(\d+)/100",
        r"\|\s*Realism\s+Score\s*\|\s*(\d+)/100",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def _parse_overall_status(text: str) -> str:
    """Extract PASS/FAIL from report."""
    # Check header first (most common format)
    header = "\n".join(text.split("\n")[:20])
    for pat in [r"\*\*Status:\*\*\s*(PASS|FAIL)", r"OVERALL\s+RESULT:\s*(PASS|FAIL)"]:
        m = re.search(pat, header, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    # Fallback: search full text for table format or summary section
    for pat in [
        r"\*\*Overall\s+Score\*\*\s*\|\s*\*\*(PASS|FAIL)\*\*",
        r"OVERALL\s+RESULT:\s*(PASS|FAIL)",
        r"\|\s*Overall\s+Score\s*\|\s*\*?\*?(PASS|FAIL)",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    return ""


def _parse_fixes_applied(text: str) -> int | None:
    """Extract number of fixes from report."""
    m = re.search(r"\*\*Fixes\s+Applied:\*\*\s*(\d+)", text[:2000], re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None


def _parse_entities_swept(text: str) -> int | None:
    """Extract entity count from report."""
    m = re.search(r"\*\*Entities:\*\*\s*(\d+)", text[:500], re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Fallback: count rows in "Entities Swept" table
    ent_section = re.search(r"##\s*Entities\s+Swept\s*\n+(\|.+\n)+", text[:2000], re.IGNORECASE)
    if ent_section:
        rows = [
            row
            for row in ent_section.group(0).split("\n")
            if row.strip().startswith("|") and "---" not in row and "Entity" not in row
        ]
        if rows:
            return len(rows)
    return None


def _parse_station_summary(text: str) -> dict:
    """Parse deep station and surface scan pass/fail/blocked counts."""
    result = {
        "deep_pass": 0,
        "deep_blocked": 0,
        "deep_total": 12,
        "surface_ok": 0,
        "surface_empty": 0,
        "surface_404": 0,
    }

    # Count deep station results from table rows with D01-D12 patterns
    # Scans ALL lines starting with | that contain station IDs (first entity = parent)
    first_entity_done = False
    for line in text.split("\n"):
        if not line.strip().startswith("|"):
            continue
        # Match station rows: "| D01 ..." or "| D01 Dashboard |"
        if re.search(r"\|\s*D(?:0[1-9]|1[0-2])\b", line):
            if "PASS" in line or "\u2713" in line:
                result["deep_pass"] += 1
            elif "BLOCKED" in line or "\u2717" in line:
                result["deep_blocked"] += 1
            elif "\u26a0" in line:  # ⚠ warning but still checked
                result["deep_pass"] += 1
            elif "\u25cb" in line:  # ○ empty but checked
                result["deep_pass"] += 1
        # Stop after first section header for next entity
        if re.search(r"#{2,3}\s+(?:Entity|Child|Summit|Ether|Apex|Global|Road)", line) and result["deep_pass"] > 0:
            first_entity_done = True
        if first_entity_done and re.search(r"\|\s*D01\b", line):
            break  # stop counting at second entity

    # Surface scan summary: ✓16 ○6 ✗8
    surf = re.search(r"\u2713(\d+).*?\u25CB(\d+).*?\u2717(\d+)", text)
    if surf:
        result["surface_ok"] = int(surf.group(1))
        result["surface_empty"] = int(surf.group(2))
        result["surface_404"] = int(surf.group(3))
    else:
        # Alt format: **Summary:** ✓16 ○6 ✗8
        surf_section = (
            text[text.find("Surface") :]
            if "Surface" in text
            else text[text.find("SURFACE") :]
            if "SURFACE" in text
            else ""
        )
        surf2 = re.search(r"(\d+).*?(\d+).*?(\d+)", surf_section[:500]) if surf_section else None
        if surf2:
            result["surface_ok"] = int(surf2.group(1))
            result["surface_empty"] = int(surf2.group(2))
            result["surface_404"] = int(surf2.group(3))

    return result


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
    # Also extract from KEY FINDINGS / KEY OBSERVATIONS section (common in v4.0+ reports)
    findings_section = re.search(
        r"##\s*KEY\s+(?:FINDINGS|OBSERVATIONS)\s*\n+((?:(?:\d+\.\s+.+|[ \t]*)\n?)+)", text, re.IGNORECASE
    )
    if findings_section:
        for line in findings_section.group(1).strip().split("\n"):
            line = re.sub(r"^\d+\.\s+", "", line).strip().rstrip("*")
            if line and line not in findings:
                findings.append(line)
    # Extract from "FIXES NEEDED" section (Summit v4.0+ format)
    fixes_needed = re.search(r"##\s*FIXES\s+NEEDED[^\n]*\n+((?:\d+\.\s+.+\n?)+)", text, re.IGNORECASE)
    if fixes_needed:
        for line in fixes_needed.group(1).strip().split("\n"):
            line = re.sub(r"^\d+\.\s+", "", line).strip().rstrip("*")
            if line and line not in findings:
                findings.append(line)
    # Extract inline ⚠ FINDING markers from station checks (e.g. "[D02] P&L ⚠ FINDING")
    for m in re.finditer(r"\*\*\[([A-Z]\d+)\]\s*([^*]+)\*\*\s*⚠\s*FINDING", text):
        tag = f"[{m.group(1)}] {m.group(2).strip()}"
        # Grab the first detail bullet after the finding marker
        pos = m.end()
        detail_match = re.search(r"\n\s*[-*]\s*\*\*(.+?)\*\*", text[pos : pos + 200])
        finding = f"{tag}: {detail_match.group(1).strip()}" if detail_match else tag
        if finding not in findings:
            findings.append(finding)
    # Extract Content Safety FLAG/WARN from CS tables (e.g. "| CS6 | ... | FLAG | ...")
    for m in re.finditer(r"\|\s*(CS\d+)\s*\|[^|]*\|\s*(?:FLAG|WARN)\s*\|\s*([^|]+)\|", text):
        finding = f"[{m.group(1)}] {m.group(2).strip()}"
        if finding not in findings:
            findings.append(finding)
    # Extract Summary bullet issues (e.g. "- **1 known IES routing issue** (...)")
    summary_section = re.search(r"##\s*Summary\s*\n+((?:\s*[-*]\s+.+\n?)+)", text, re.IGNORECASE)
    if summary_section:
        for line in summary_section.group(1).strip().split("\n"):
            line = line.strip().lstrip("-* ").strip()
            line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)  # strip bold markers
            # Only capture lines that mention issues/warnings/flags (not positive "all pass" lines)
            if line and re.search(r"issue|warning|flag|negative|error|block|fail|404|swap", line, re.IGNORECASE):
                if line not in findings:
                    findings.append(line)
    # Final cleanup: strip remaining markdown bold markers from all findings
    findings = [re.sub(r"\*\*(.+?)\*\*", r"\1", f) for f in findings]
    findings = [f.replace("**", "") for f in findings]  # catch orphaned **
    return findings


def _extract_shortcode_from_filename(stem: str) -> str:
    """Extract shortcode from report filename like 'mid_market_v2_2026-03-06'.

    Gets everything before the date pattern, strips version/session suffixes,
    and normalizes underscores to hyphens to match credential shortcodes.
    """
    m = re.match(r"(.+?)_(\d{4}-\d{2}-\d{2})", stem)
    if not m:
        return ""
    prefix = m.group(1).lower()
    # Strip known suffixes that are session labels, not part of shortcode
    prefix = re.sub(r"_(?:v\d+|revalidation|fix_session|PARTIAL)$", "", prefix, flags=re.IGNORECASE)
    return prefix.replace("_", "-")


_email_sc_cache: dict = {"data": {}, "ts": 0}


def _get_email_to_shortcode_map() -> dict[str, str]:
    """Load {email: shortcode} from credentials. Cached for CACHE_TTL."""
    now = time.time()
    if _email_sc_cache["data"] and (now - _email_sc_cache["ts"]) < CACHE_TTL:
        return _email_sc_cache["data"]

    mapping: dict[str, str] = {}
    try:
        with open(CREDENTIALS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        for email, info in data.get("accounts", {}).items():
            sc = info.get("shortcode", "").lower()
            if sc:
                mapping[email.lower()] = sc
                for alt in info.get("alt_credentials", []):
                    if alt.get("email"):
                        mapping[alt["email"].lower()] = sc
    except Exception:
        pass

    _email_sc_cache["data"] = mapping
    _email_sc_cache["ts"] = now
    return mapping


def _load_sweep_reports() -> dict[str, SweepResult]:
    """Load and parse all sweep reports, keyed by shortcode AND email."""
    results: dict[str, SweepResult] = {}
    if not SWEEP_DIR.exists():
        return results

    for f in sorted(SWEEP_DIR.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")

        # Extract shortcode from filename (e.g. mid_market_v2_2026-03-06.md → mid-market)
        shortcode_from_file = _extract_shortcode_from_filename(f.stem)

        # Extract email from Account line (strips backticks, parens)
        email_match = re.search(r"\*\*Account:\*\*\s*(?:\w+\s*)?[(\`]?(\S+@\S+?)[)\`]?(?:\s|$)", text[:500])
        email = email_match.group(1).strip().strip("`).") if email_match else ""

        # Extract shortcode from Account line (e.g. "**Account:** summit" or "**Account:** TCO (...)")
        sc_match = re.search(r"\*\*Account:\*\*\s*(\w+)", text[:500])
        shortcode_from_text = sc_match.group(1).lower() if sc_match else ""

        score = _parse_sweep_score(text)
        date = _parse_sweep_date(text) or ""
        p1s = _parse_p1_findings(text)
        realism = _parse_realism_score(text)
        status = _parse_overall_status(text)
        fixes = _parse_fixes_applied(text)
        entities = _parse_entities_swept(text)
        stations = _parse_station_summary(text)

        sweep = SweepResult(
            date=date,
            score=score,
            report_file=f.name,
            p1_findings=p1s,
            realism_score=realism,
            overall_status=status,
            fixes_applied=fixes,
            entities_swept=entities,
            **stations,
        )

        # Store by all possible keys (email, shortcode from file, shortcode from text)
        keys = set()
        if email:
            keys.add(email)
        if shortcode_from_file:
            keys.add(f"sc:{shortcode_from_file}")
        if shortcode_from_text:
            keys.add(f"sc:{shortcode_from_text}")

        for key in keys:
            existing = results.get(key)
            if existing is None or date >= existing.date:
                results[key] = sweep

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
        shortcode = info.get("shortcode", "")
        sweep = sweep_reports.get(email) or sweep_reports.get(f"sc:{shortcode.lower()}")
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

    # Sort: most accessed workspace first, then by sweep health desc
    accounts.sort(
        key=lambda a: (
            -a.total_accesses,
            0 if a.sweep and (a.sweep.realism_score or a.sweep.score) else 1,
            -(a.sweep.realism_score if a.sweep and a.sweep.realism_score else 0),
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


# ─── Sweep History & Delta ───

_history_cache: dict = {"data": {}, "ts": 0}


def _build_history_index() -> dict[str, list[SweepHistoryEntry]]:
    """Parse all sweep reports, group by shortcode key. Cached for CACHE_TTL."""
    now = time.time()
    if _history_cache["data"] and (now - _history_cache["ts"]) < CACHE_TTL:
        return _history_cache["data"]

    index: dict[str, list[SweepHistoryEntry]] = {}
    if not SWEEP_DIR.exists():
        return index

    email_sc_map = _get_email_to_shortcode_map()

    for f in sorted(SWEEP_DIR.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")

        # Extract shortcode from filename (e.g. mid_market_v2_2026-03-06 → mid-market)
        shortcode_from_file = _extract_shortcode_from_filename(f.stem)

        # Extract email and resolve to shortcode via credentials
        email_match = re.search(r"\*\*Account:\*\*\s*.*?([\w.\-]+@[\w.\-]+)", text[:500])
        email = email_match.group(1).lower() if email_match else ""
        shortcode_from_email = email_sc_map.get(email, "")

        # Extract shortcode from Account line text (plain word before email)
        sc_match = re.search(r"\*\*Account:\*\*\s*(\w+)", text[:500])
        shortcode_from_text = sc_match.group(1).lower() if sc_match else ""
        # Normalize underscore to hyphen
        shortcode_from_text = shortcode_from_text.replace("_", "-")

        keys = set()
        if shortcode_from_email:
            keys.add(shortcode_from_email)
        if shortcode_from_file:
            keys.add(shortcode_from_file)
        if shortcode_from_text and shortcode_from_text not in (
            "quickbooks",
            "mid",
            "qsp",
        ):
            keys.add(shortcode_from_text)
        if not keys:
            continue

        # Parse metrics
        date = _parse_sweep_date(text) or ""
        score = _parse_sweep_score(text)
        realism = _parse_realism_score(text)
        status = _parse_overall_status(text)
        fixes = _parse_fixes_applied(text)
        stations = _parse_station_summary(text)
        p1s = _parse_p1_findings(text)

        # Compute display_health (same formula as SweepResult.display_health)
        health = None
        if realism is not None:
            health = min(realism + 20, 100)
        elif score is not None:
            health = min(int(score * 10) + 20, 100)

        entry = SweepHistoryEntry(
            date=date,
            health=health,
            realism_score=realism,
            score=score,
            overall_status=status,
            fixes_applied=fixes,
            p1_findings=p1s,
            report_file=f.name,
            deep_pass=stations["deep_pass"],
            surface_ok=stations["surface_ok"],
            surface_404=stations["surface_404"],
        )

        for key in keys:
            index.setdefault(key, []).append(entry)

    # Sort each group by date, deduplicate same date (keep higher health)
    for key in index:
        index[key].sort(key=lambda e: (e.date, -(e.health or 0)))
        seen: set[str] = set()
        unique: list[SweepHistoryEntry] = []
        for e in index[key]:
            if e.date not in seen:
                seen.add(e.date)
                unique.append(e)
        index[key] = unique

    _history_cache["data"] = index
    _history_cache["ts"] = now
    return index


def load_sweep_history(shortcode: str) -> list[SweepHistoryEntry]:
    """Get all sweep reports for an account, sorted oldest to newest."""
    index = _build_history_index()
    return index.get(shortcode.lower(), [])


def compute_sweep_delta(shortcode: str) -> dict | None:
    """Compare last two sweeps for an account. Returns None if <2 sweeps."""
    history = load_sweep_history(shortcode)
    if len(history) < 2:
        return None

    prev, curr = history[-2], history[-1]

    health_delta = None
    if curr.health is not None and prev.health is not None:
        health_delta = curr.health - prev.health

    direction = "up" if (health_delta or 0) > 0 else "down" if (health_delta or 0) < 0 else "stable"
    arrow = "\u2191" if direction == "up" else "\u2193" if direction == "down" else "\u2192"

    prev_findings = set(prev.p1_findings)
    curr_findings = set(curr.p1_findings)

    return {
        "prev_date": prev.date,
        "curr_date": curr.date,
        "prev_health": prev.health,
        "curr_health": curr.health,
        "health_delta": health_delta,
        "direction": direction,
        "arrow": arrow,
        "prev_status": prev.overall_status,
        "curr_status": curr.overall_status,
        "fixes_delta": (curr.fixes_applied or 0) - (prev.fixes_applied or 0),
        "deep_pass_delta": curr.deep_pass - prev.deep_pass,
        "surface_ok_delta": curr.surface_ok - prev.surface_ok,
        "new_findings": [classify_finding(f) for f in curr_findings - prev_findings],
        "resolved_findings": [classify_finding(f) for f in prev_findings - curr_findings],
        "persistent_findings": [classify_finding(f) for f in curr_findings & prev_findings],
    }
