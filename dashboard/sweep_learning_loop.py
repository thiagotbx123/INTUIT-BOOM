"""Sweep Learning Loop — Dynamic evolution system for the QBO Demo Manager.

v1.0 — 2026-03-26
A feedback loop that makes the sweep smarter with each run. No ML — just a
structured dictionary that accumulates findings, ranks fix effectiveness,
and advises future sweeps on what to prioritize.

Audit fixes incorporated from AUDIT_sweep_learning_loop_20260326.xlsx:
- A23-001 HIGH: Backup rotation before each save (3 backups kept)
- A09-001 MEDIUM: Minimum attempts threshold for fix ranking
- A01-001 MEDIUM: try/except on JSON load with .bak recovery
- A02-001 MEDIUM: try/except on save with fallback path
- A03-001 MEDIUM: Instance path instead of global mutable state
- A11-001 LOW: failure_reasons capped at 20
- A29-001 LOW: Schema versioning for future migrations
- A07-001 LOW: Configurable paths via env vars

Usage:
    from sweep_learning_loop import SweepLearner

    learner = SweepLearner()                    # default path
    learner = SweepLearner("/custom/path.json")  # custom path

    # After each station:
    learner.record_finding("D05", "construction", "CS3", "placeholder_name",
                           fix_applied="renamed to Harbor Point Estates",
                           fix_success=True)

    # After a fix:
    learner.record_fix("FIX-03", "rename_placeholder", success=True,
                       context={"station": "D05", "entity": "Keystone Construction"})

    # Before starting a station — get advice:
    advice = learner.advise("D05", "construction")
    # Returns: {"priority_findings": [...], "recommended_fixes": [...], "watch_for": [...]}

    # Bootstrap from existing sweep reports:
    learner.bootstrap_from_reports("/path/to/sweep-learnings/")
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Schema version — increment when structure changes
SCHEMA_VERSION = 1

# Minimum attempts before a fix is eligible for "best" ranking (A09-001)
MIN_ATTEMPTS_THRESHOLD = 3

# Max failure reasons stored per fix (A11-001)
MAX_FAILURE_REASONS = 20

# Max backups to keep (A23-001)
MAX_BACKUPS = 3

# Default path — configurable via env var (A07-001)
DEFAULT_LEARNINGS_PATH = Path(
    os.environ.get(
        "SWEEP_LEARNINGS_PATH",
        str(Path(__file__).resolve().parent / "sweep_learnings.json"),
    )
)


def _empty_learnings():
    """Return a fresh learnings structure with schema version."""
    return {
        "schema_version": SCHEMA_VERSION,
        "meta": {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_sweeps_processed": 0,
            "total_findings_recorded": 0,
            "total_fixes_recorded": 0,
        },
        "findings": {},
        "fixes": {},
        "station_patterns": {},
        "sector_patterns": {},
    }


def _migrate_schema(data):
    """Migrate old schema versions to current. Returns migrated data."""
    version = data.get("schema_version", 0)
    if version == SCHEMA_VERSION:
        return data
    if version == 0:
        # Pre-versioning: add schema_version and meta
        data["schema_version"] = SCHEMA_VERSION
        if "meta" not in data:
            data["meta"] = {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_sweeps_processed": 0,
                "total_findings_recorded": 0,
                "total_fixes_recorded": 0,
            }
        return data
    return data


def load_learnings(path):
    """Load learnings from JSON file. Handles corrupt files gracefully (A01-001)."""
    path = Path(path)
    if not path.exists():
        return _empty_learnings()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return _migrate_schema(data)
    except (json.JSONDecodeError, ValueError) as e:
        # A01-001: Don't crash on corrupt JSON — backup and start fresh
        bak = path.with_suffix(f".corrupt.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")
        try:
            shutil.copy2(path, bak)
        except OSError:
            pass
        print(f"WARNING: Corrupt learnings file at {path}. Backed up to {bak}. Error: {e}")
        return _empty_learnings()
    except OSError as e:
        print(f"WARNING: Cannot read learnings file at {path}. Error: {e}")
        return _empty_learnings()


def _rotate_backups(path):
    """Keep last N backups before saving (A23-001)."""
    path = Path(path)
    bak = path.with_suffix(".json.bak")
    # Rotate: .bak.2 → .bak.3, .bak.1 → .bak.2, .bak → .bak.1
    for i in range(MAX_BACKUPS, 1, -1):
        old = path.with_suffix(f".json.bak.{i - 1}")
        new = path.with_suffix(f".json.bak.{i}")
        if old.exists():
            try:
                shutil.move(str(old), str(new))
            except OSError:
                pass
    if bak.exists():
        try:
            shutil.move(str(bak), path.with_suffix(".json.bak.1"))
        except OSError:
            pass
    # Current → .bak
    if path.exists():
        try:
            shutil.copy2(path, bak)
        except OSError:
            pass


def save_learnings(data, path):
    """Save learnings to JSON with backup rotation (A02-001, A23-001)."""
    path = Path(path)
    data["meta"]["last_updated"] = datetime.now().isoformat()

    # Rotate backups before saving
    _rotate_backups(path)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        # A02-001: Fallback path
        fallback = Path.home() / "sweep_learnings_fallback.json"
        print(f"WARNING: Cannot save to {path}. Trying fallback {fallback}. Error: {e}")
        try:
            with open(fallback, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as e2:
            print(f"CRITICAL: Cannot save learnings anywhere. Data lost for this run. Error: {e2}")


def record_finding(data, station, sector, finding_type, description, fix_applied=None, fix_success=None):
    """Record a finding from a sweep station.

    Args:
        data: Learnings dict
        station: Station ID (e.g. "D05")
        sector: Dataset sector (e.g. "construction")
        finding_type: Category (e.g. "CS3", "data_gap", "ui_broken")
        description: What was found
        fix_applied: Fix description if applied
        fix_success: True/False if fix was applied
    """
    key = f"{station}:{finding_type}"

    if key not in data["findings"]:
        data["findings"][key] = {
            "station": station,
            "sector": sector,
            "finding_type": finding_type,
            "description": description,
            "occurrences": 0,
            "last_seen": None,
            "fixed_count": 0,
            "unfixed_count": 0,
            "sectors_seen": [],
        }

    finding = data["findings"][key]
    finding["occurrences"] += 1
    finding["last_seen"] = datetime.now().isoformat()
    finding["description"] = description  # Update with latest description

    if sector not in finding["sectors_seen"]:
        finding["sectors_seen"].append(sector)

    if fix_applied and fix_success:
        finding["fixed_count"] += 1
    elif fix_applied and not fix_success:
        finding["unfixed_count"] += 1

    # Station patterns
    if station not in data["station_patterns"]:
        data["station_patterns"][station] = {"total_findings": 0, "top_types": {}}
    data["station_patterns"][station]["total_findings"] += 1
    types = data["station_patterns"][station]["top_types"]
    types[finding_type] = types.get(finding_type, 0) + 1

    # Sector patterns
    if sector not in data["sector_patterns"]:
        data["sector_patterns"][sector] = {"total_findings": 0, "top_stations": {}}
    data["sector_patterns"][sector]["total_findings"] += 1
    stations = data["sector_patterns"][sector]["top_stations"]
    stations[station] = stations.get(station, 0) + 1

    data["meta"]["total_findings_recorded"] += 1


def record_fix(data, fix_id, fix_type, success, context=None):
    """Record a fix attempt and its outcome.

    Args:
        data: Learnings dict
        fix_id: Fix protocol ID (e.g. "FIX-03")
        fix_type: Fix category (e.g. "rename_placeholder")
        success: True if fix worked, False if failed
        context: Optional dict with station, entity, failure_reason, etc.
    """
    context = context or {}

    if fix_id not in data["fixes"]:
        data["fixes"][fix_id] = {
            "fix_type": fix_type,
            "attempts": 0,
            "successes": 0,
            "failures": 0,
            "success_rate": 0.0,
            "last_used": None,
            "failure_reasons": [],
            "stations_used": [],
            "sectors_used": [],
        }

    fix = data["fixes"][fix_id]
    fix["attempts"] += 1
    fix["last_used"] = datetime.now().isoformat()

    if success:
        fix["successes"] += 1
    else:
        fix["failures"] += 1
        reason = context.get("failure_reason", "unknown")
        fix["failure_reasons"].append(reason)
        # A11-001: Cap failure reasons
        if len(fix["failure_reasons"]) > MAX_FAILURE_REASONS:
            fix["failure_reasons"] = fix["failure_reasons"][-MAX_FAILURE_REASONS:]

    # Calculate success rate
    fix["success_rate"] = round(fix["successes"] / fix["attempts"], 3)

    # Track where fix was used
    station = context.get("station")
    if station and station not in fix["stations_used"]:
        fix["stations_used"].append(station)

    sector = context.get("sector")
    if sector and sector not in fix["sectors_used"]:
        fix["sectors_used"].append(sector)

    data["meta"]["total_fixes_recorded"] += 1


def advise(data, station, sector):
    """Get advice for a station based on accumulated learnings.

    Returns:
        dict with:
        - priority_findings: Most common findings for this station+sector
        - recommended_fixes: Best fixes for findings likely to appear
        - watch_for: Patterns to look out for
        - confidence: How much data backs this advice (low/medium/high)
    """
    advice = {
        "priority_findings": [],
        "recommended_fixes": [],
        "watch_for": [],
        "confidence": "low",
    }

    # Find relevant findings for this station
    station_findings = []
    for key, finding in data.get("findings", {}).items():
        if finding["station"] == station:
            station_findings.append(finding)
        elif sector in finding.get("sectors_seen", []):
            # Also include findings from other stations in the same sector
            station_findings.append(finding)

    # Sort by occurrences (most common first)
    station_findings.sort(key=lambda x: x["occurrences"], reverse=True)
    advice["priority_findings"] = station_findings[:5]

    # Find best fixes — A09-001: only rank fixes with enough attempts
    eligible_fixes = []
    for fix_id, fix in data.get("fixes", {}).items():
        if station in fix.get("stations_used", []) or sector in fix.get("sectors_used", []):
            if fix["attempts"] >= MIN_ATTEMPTS_THRESHOLD:
                eligible_fixes.append({"fix_id": fix_id, **fix})
            elif fix["attempts"] > 0:
                # Below threshold — include but flag as "untested"
                eligible_fixes.append({"fix_id": fix_id, **fix, "_untested": True})

    # Sort: tested fixes by success_rate first, untested at the end
    tested = [f for f in eligible_fixes if not f.get("_untested")]
    untested = [f for f in eligible_fixes if f.get("_untested")]
    tested.sort(key=lambda x: (x["success_rate"], x["attempts"]), reverse=True)
    untested.sort(key=lambda x: x["attempts"], reverse=True)
    advice["recommended_fixes"] = tested[:3] + untested[:2]

    # Watch-for patterns from sector patterns
    sector_data = data.get("sector_patterns", {}).get(sector, {})
    top_stations = sector_data.get("top_stations", {})
    if station in top_stations and top_stations[station] >= 3:
        advice["watch_for"].append(
            f"Station {station} has {top_stations[station]} historical findings in {sector} — high attention needed"
        )

    # Station pattern warnings
    station_data = data.get("station_patterns", {}).get(station, {})
    top_types = station_data.get("top_types", {})
    for ftype, count in sorted(top_types.items(), key=lambda x: x[1], reverse=True)[:3]:
        if count >= 2:
            advice["watch_for"].append(f"Common finding type: {ftype} ({count}x in {station})")

    # Confidence based on data volume
    total = data.get("meta", {}).get("total_findings_recorded", 0)
    if total >= 50:
        advice["confidence"] = "high"
    elif total >= 15:
        advice["confidence"] = "medium"
    else:
        advice["confidence"] = "low"

    return advice


def get_sweep_summary(data):
    """Generate a summary of all accumulated learnings.

    Returns:
        dict with top findings, best fixes, problem stations, sector insights
    """
    summary = {
        "total_findings": data.get("meta", {}).get("total_findings_recorded", 0),
        "total_fixes": data.get("meta", {}).get("total_fixes_recorded", 0),
        "total_sweeps": data.get("meta", {}).get("total_sweeps_processed", 0),
        "top_findings": [],
        "best_fixes": [],
        "worst_fixes": [],
        "problem_stations": [],
        "sector_insights": {},
    }

    # Top findings by occurrence
    findings_list = list(data.get("findings", {}).values())
    findings_list.sort(key=lambda x: x["occurrences"], reverse=True)
    summary["top_findings"] = findings_list[:10]

    # Best and worst fixes (only with enough attempts)
    fixes_list = [
        {"fix_id": k, **v} for k, v in data.get("fixes", {}).items() if v["attempts"] >= MIN_ATTEMPTS_THRESHOLD
    ]
    fixes_list.sort(key=lambda x: x["success_rate"], reverse=True)
    summary["best_fixes"] = fixes_list[:5]
    summary["worst_fixes"] = fixes_list[-3:] if len(fixes_list) >= 3 else []

    # Problem stations (most findings)
    station_list = [{"station": k, **v} for k, v in data.get("station_patterns", {}).items()]
    station_list.sort(key=lambda x: x["total_findings"], reverse=True)
    summary["problem_stations"] = station_list[:5]

    # Sector insights
    for sector, sdata in data.get("sector_patterns", {}).items():
        summary["sector_insights"][sector] = {
            "total_findings": sdata.get("total_findings", 0),
            "top_station": max(sdata.get("top_stations", {"?": 0}).items(), key=lambda x: x[1])[0]
            if sdata.get("top_stations")
            else "none",
        }

    return summary


def bootstrap_from_reports(data, reports_dir):
    """Bootstrap learnings from existing sweep report markdown files.

    Parses the depth protocol format:
        ### DXX — Name — Score: X/10
        **Findings:** ...
        **Fixes:** ...

    Args:
        data: Learnings dict to populate
        reports_dir: Path to sweep-learnings directory
    """
    reports_dir = Path(reports_dir)
    if not reports_dir.exists():
        print(f"WARNING: Reports directory not found: {reports_dir}")
        return 0

    count = 0
    for report_file in sorted(reports_dir.glob("*.md")):
        try:
            content = report_file.read_text(encoding="utf-8")
        except OSError:
            continue

        # Extract sector from report header
        sector_match = re.search(r"\*\*Dataset:\*\*\s*(\w+)", content)
        sector = sector_match.group(1) if sector_match else "unknown"

        # Find station sections
        station_pattern = re.compile(r"###\s+(D\d+|S\d+|C\d+|X\d+)\s+.+?Score:\s*(\d+(?:\.\d+)?)/10", re.MULTILINE)
        sections = list(station_pattern.finditer(content))

        for i, match in enumerate(sections):
            station = match.group(1)
            # Get section text until next station or end
            start = match.end()
            end = sections[i + 1].start() if i + 1 < len(sections) else len(content)
            section_text = content[start:end]

            # Extract findings
            findings_match = re.search(r"\*\*Findings:\*\*\s*(.*?)(?:\*\*|$)", section_text, re.DOTALL)
            if findings_match:
                findings_text = findings_match.group(1).strip()
                if findings_text and findings_text.upper() != "CLEAN" and findings_text.upper() != "NONE":
                    # Parse individual findings (P1/P2/P3 lines)
                    for line in findings_text.split("\n"):
                        line = line.strip().lstrip("- ")
                        if line and len(line) > 5:
                            ftype = "P1" if "P1" in line else "P2" if "P2" in line else "P3"
                            record_finding(data, station, sector, ftype, line)
                            count += 1

            # Extract fixes
            fixes_match = re.search(r"\*\*Fixes:\*\*\s*(.*?)(?:\*\*|$)", section_text, re.DOTALL)
            if fixes_match:
                fixes_text = fixes_match.group(1).strip()
                if fixes_text and fixes_text.upper() != "NONE":
                    for line in fixes_text.split("\n"):
                        line = line.strip().lstrip("- ")
                        if line and len(line) > 5:
                            # Determine fix type from content
                            fix_type = "unknown"
                            if "renamed" in line.lower() or "renomear" in line.lower():
                                fix_type = "rename_placeholder"
                            elif "enriched" in line.lower() or "added" in line.lower():
                                fix_type = "enrichment"
                            elif "je" in line.lower() or "journal" in line.lower():
                                fix_type = "journal_entry"
                            elif "categoriz" in line.lower():
                                fix_type = "categorize_txn"
                            elif "paid" in line.lower() or "payment" in line.lower():
                                fix_type = "pay_bill"
                            record_fix(
                                data,
                                f"FIX-{fix_type}",
                                fix_type,
                                success=True,
                                context={"station": station, "sector": sector},
                            )
                            count += 1

        data["meta"]["total_sweeps_processed"] += 1

    if count == 0:
        print(f"WARNING: Zero findings extracted from {reports_dir}. Check report format.")

    return count


class SweepLearner:
    """High-level interface for the sweep learning loop.

    Usage:
        learner = SweepLearner()
        learner.record_finding("D05", "construction", "CS3", "placeholder name found")
        advice = learner.advise("D05", "construction")
        learner.save()
    """

    def __init__(self, learnings_path=None):
        """Initialize with optional custom path (A03-001: instance var, not global)."""
        self._path = Path(learnings_path) if learnings_path else DEFAULT_LEARNINGS_PATH
        self._data = load_learnings(self._path)

    def record_finding(self, station, sector, finding_type, description, fix_applied=None, fix_success=None):
        """Record a finding. See module-level record_finding for docs."""
        record_finding(self._data, station, sector, finding_type, description, fix_applied, fix_success)

    def record_fix(self, fix_id, fix_type, success, context=None):
        """Record a fix attempt. See module-level record_fix for docs."""
        record_fix(self._data, fix_id, fix_type, success, context)

    def advise(self, station, sector):
        """Get advice for a station. See module-level advise for docs."""
        return advise(self._data, station, sector)

    def get_summary(self):
        """Get accumulated learning summary. See module-level get_sweep_summary for docs."""
        return get_sweep_summary(self._data)

    def bootstrap_from_reports(self, reports_dir):
        """Bootstrap from existing sweep reports. See module-level function for docs."""
        count = bootstrap_from_reports(self._data, reports_dir)
        if count > 0:
            self.save()
        return count

    def save(self):
        """Persist learnings to disk with backup rotation."""
        save_learnings(self._data, self._path)

    @property
    def data(self):
        """Access raw learnings data (read-only intent)."""
        return self._data

    @property
    def path(self):
        """Current learnings file path."""
        return self._path


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sweep_learning_loop.py bootstrap [reports_dir]")
        print("  python sweep_learning_loop.py summary")
        print("  python sweep_learning_loop.py advise <station> <sector>")
        sys.exit(1)

    command = sys.argv[1]
    learner = SweepLearner()

    if command == "bootstrap":
        reports_dir = (
            sys.argv[2]
            if len(sys.argv) > 2
            else os.environ.get(
                "SWEEP_REPORTS_DIR",
                str(Path(__file__).resolve().parent.parent / "knowledge-base" / "sweep-learnings"),
            )
        )
        count = learner.bootstrap_from_reports(reports_dir)
        print(f"Bootstrapped {count} findings/fixes from {reports_dir}")
        print(f"Learnings saved to {learner.path}")

    elif command == "summary":
        summary = learner.get_summary()
        print(f"Total findings: {summary['total_findings']}")
        print(f"Total fixes: {summary['total_fixes']}")
        print(f"Total sweeps: {summary['total_sweeps']}")
        if summary["problem_stations"]:
            print("\nProblem stations:")
            for s in summary["problem_stations"]:
                print(f"  {s['station']}: {s['total_findings']} findings")
        if summary["best_fixes"]:
            print("\nBest fixes:")
            for f in summary["best_fixes"]:
                print(f"  {f['fix_id']}: {f['success_rate'] * 100:.0f}% ({f['attempts']} attempts)")

    elif command == "advise":
        if len(sys.argv) < 4:
            print("Usage: python sweep_learning_loop.py advise <station> <sector>")
            sys.exit(1)
        station = sys.argv[2]
        sector = sys.argv[3]
        advice = learner.advise(station, sector)
        print(f"Advice for {station} ({sector}):")
        print(f"  Confidence: {advice['confidence']}")
        if advice["priority_findings"]:
            print("  Priority findings:")
            for f in advice["priority_findings"]:
                print(f"    - {f['finding_type']}: {f['description'][:80]} ({f['occurrences']}x)")
        if advice["watch_for"]:
            print("  Watch for:")
            for w in advice["watch_for"]:
                print(f"    - {w}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
