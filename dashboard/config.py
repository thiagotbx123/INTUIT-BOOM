"""Sweep config management — load, save, profiles."""

import json
from pathlib import Path

from sweep_checks import (
    CONDITIONAL_CHECKS,
    CONTENT_SAFETY,
    DEEP_STATIONS,
    FIX_TIERS,
    REVALIDATION_RULES,
    SURFACE_SCAN,
    get_all_checks,
    get_default_profile,
)

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)

PROFILES_FILE = CONFIG_DIR / "profiles.json"
ACCOUNT_CONFIGS_FILE = CONFIG_DIR / "account_configs.json"


def _load_json(path: Path, default=None):
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            # Corrupted JSON — return default to allow auto-regeneration
            return default if default is not None else {}
    return default if default is not None else {}


def _save_json(path: Path, data):
    # Atomic write: write to temp file, then rename to prevent corruption on crash
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(path)


# --- Profiles ---


def load_profiles() -> dict:
    """Load saved sweep profiles."""
    profiles = _load_json(PROFILES_FILE, {})
    # Always ensure default exists and is up-to-date
    current_default = get_default_profile()
    if (
        "full_sweep" not in profiles
        or profiles["full_sweep"].get("name") != current_default["name"]
        or profiles["full_sweep"].get("description") != current_default["description"]
    ):
        profiles["full_sweep"] = current_default
        _save_json(PROFILES_FILE, profiles)
    # Regenerate built-in profiles if check counts changed (detect stale profiles)
    _expected_surface_count = len(SURFACE_SCAN)
    _qs_stale = (
        "quick_sweep" in profiles
        and len([k for k in profiles["quick_sweep"].get("checks", {}) if k.startswith("S")]) < _expected_surface_count
    )
    if "quick_sweep" not in profiles or _qs_stale:
        profiles["quick_sweep"] = {
            "name": "Quick Sweep",
            "description": "Core financial health only (D01-D06 + Surface)",
            "checks": {
                **{s["id"]: int(s["id"][1:]) <= 6 for s in DEEP_STATIONS},
                **{s["id"]: True for s in SURFACE_SCAN},
                **{s["id"]: False for s in CONDITIONAL_CHECKS},
            },
            "fix_tiers": {"fix_immediately": True, "fix_and_report": False, "never_fix": False},
            "content_safety": {c["id"]: True for c in CONTENT_SAFETY},
            "realism_scoring": False,
        }
    _so_stale = (
        "surface_only" in profiles
        and len([k for k in profiles["surface_only"].get("checks", {}) if k.startswith("S")]) < _expected_surface_count
    )
    if "surface_only" not in profiles or _so_stale:
        profiles["surface_only"] = {
            "name": "Surface Only",
            "description": "Surface pages — no corrections, fast scan",
            "checks": {
                **{s["id"]: False for s in DEEP_STATIONS},
                **{s["id"]: True for s in SURFACE_SCAN},
                **{s["id"]: False for s in CONDITIONAL_CHECKS},
            },
            "fix_tiers": {"fix_immediately": False, "fix_and_report": False, "never_fix": False},
            "content_safety": {c["id"]: True for c in CONTENT_SAFETY},
            "realism_scoring": False,
        }
    # Reconcile all profiles — add any new checks/content_safety that code defines but JSON doesn't have
    all_check_ids = {c["id"] for c in get_all_checks()}
    all_cs_ids = {c["id"] for c in CONTENT_SAFETY}
    all_rv_ids = {r["id"] for r in REVALIDATION_RULES}
    dirty = False
    for key, prof in profiles.items():
        # Add missing check IDs (default True for full_sweep, False for others)
        for cid in all_check_ids:
            if cid not in prof.get("checks", {}):
                prof.setdefault("checks", {})[cid] = key == "full_sweep"
                dirty = True
        # Add missing content safety IDs (default True for all profiles)
        for csid in all_cs_ids:
            if csid not in prof.get("content_safety", {}):
                prof.setdefault("content_safety", {})[csid] = True
                dirty = True
        # Add revalidation if missing
        if "revalidation" not in prof:
            prof["revalidation"] = {rid: True for rid in all_rv_ids}
            dirty = True
        else:
            for rid in all_rv_ids:
                if rid not in prof["revalidation"]:
                    prof["revalidation"][rid] = True
                    dirty = True
    if dirty:
        _save_json(PROFILES_FILE, profiles)
    return profiles


def save_profile(key: str, profile: dict):
    """Save a sweep profile."""
    profiles = load_profiles()
    profiles[key] = profile
    _save_json(PROFILES_FILE, profiles)


def delete_profile(key: str):
    """Delete a sweep profile (except defaults)."""
    if key in ("full_sweep", "quick_sweep", "surface_only"):
        return False
    profiles = load_profiles()
    profiles.pop(key, None)
    _save_json(PROFILES_FILE, profiles)
    return True


# --- Account Configs ---


def load_account_configs() -> dict:
    """Load per-account config assignments."""
    return _load_json(ACCOUNT_CONFIGS_FILE, {})


def save_account_config(shortcode: str, config: dict):
    """Save config for a specific account."""
    configs = load_account_configs()
    configs[shortcode] = config
    _save_json(ACCOUNT_CONFIGS_FILE, configs)


def get_account_config(shortcode: str) -> dict:
    """Get config for a specific account, with defaults."""
    configs = load_account_configs()
    return configs.get(
        shortcode,
        {
            "profile": "full_sweep",
            "overrides": {},
            "notes": "",
            "hidden": False,
        },
    )


# --- Prompt Generation ---


def generate_sweep_command(shortcode: str, account_label: str, account_email: str) -> str:
    """Generate the full sweep command based on account config."""
    cfg = get_account_config(shortcode)
    profile_key = cfg.get("profile", "full_sweep")
    profiles = load_profiles()
    profile = profiles.get(profile_key, get_default_profile())

    enabled_deep = [c for c in DEEP_STATIONS if profile["checks"].get(c["id"], True)]
    enabled_surface = [c for c in SURFACE_SCAN if profile["checks"].get(c["id"], True)]
    enabled_conditional = [c for c in CONDITIONAL_CHECKS if profile["checks"].get(c["id"], True)]

    fix_mode = []
    for tier, enabled in profile.get("fix_tiers", {}).items():
        if enabled:
            fix_mode.append(FIX_TIERS[tier]["label"])

    lines = [
        f"QBO Sweep no {account_label}",
        f"Account: {account_email}",
        f"Profile: {profile['name']}",
        "",
        f"Deep Stations ({len(enabled_deep)}/{len(DEEP_STATIONS)}):",
    ]
    for c in enabled_deep:
        lines.append(f"  [{c['id']}] {c['name']}")

    lines.append("")
    lines.append(f"Surface Scan ({len(enabled_surface)}/{len(SURFACE_SCAN)}):")
    for c in enabled_surface:
        lines.append(f"  [{c['id']}] {c['name']} -> {c['route']}")

    lines.append("")
    lines.append(f"Conditional ({len(enabled_conditional)}/{len(CONDITIONAL_CHECKS)}):")
    for c in enabled_conditional:
        lines.append(f"  [{c['id']}] {c['name']} (if {c['condition']})")

    lines.append("")
    lines.append(f"Fix Mode: {', '.join(fix_mode) if fix_mode else 'Report only (no fixes)'}")

    if profile.get("realism_scoring"):
        lines.append("Demo Realism Scoring: ENABLED (10 criteria)")

    overrides = cfg.get("overrides", {})
    if overrides:
        lines.append("")
        lines.append("Account Overrides:")
        for check_id, override in overrides.items():
            lines.append(f"  {check_id}: {override}")

    notes = cfg.get("notes", "")
    if notes:
        lines.append("")
        lines.append(f"Notes: {notes}")

    return "\n".join(lines)
