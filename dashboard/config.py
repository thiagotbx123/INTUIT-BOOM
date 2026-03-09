"""Sweep config management — load, save, profiles."""

import json
from pathlib import Path

from sweep_checks import (
    CONDITIONAL_CHECKS,
    CONTENT_SAFETY,
    DEEP_STATIONS,
    FIX_TIERS,
    SURFACE_SCAN,
    get_default_profile,
)

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_DIR.mkdir(exist_ok=True)

PROFILES_FILE = CONFIG_DIR / "profiles.json"
ACCOUNT_CONFIGS_FILE = CONFIG_DIR / "account_configs.json"


def _load_json(path: Path, default=None):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default if default is not None else {}


def _save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Profiles ---


def load_profiles() -> dict:
    """Load saved sweep profiles."""
    profiles = _load_json(PROFILES_FILE, {})
    # Always ensure default exists
    if "full_sweep" not in profiles:
        profiles["full_sweep"] = get_default_profile()
    if "quick_sweep" not in profiles:
        profiles["quick_sweep"] = {
            "name": "Quick Sweep",
            "description": "Core financial health only (D01-D06 + Surface)",
            "checks": {
                **{f"D{i:02d}": i <= 6 for i in range(1, 13)},
                **{f"S{i:02d}": True for i in range(1, 21)},
                **{f"C{i:02d}": False for i in range(1, 15)},
            },
            "fix_tiers": {"fix_immediately": True, "fix_and_report": False, "never_fix": False},
            "content_safety": {c["id"]: True for c in CONTENT_SAFETY},
            "realism_scoring": False,
        }
    if "surface_only" not in profiles:
        profiles["surface_only"] = {
            "name": "Surface Only",
            "description": "20 surface pages — no corrections, fast scan",
            "checks": {
                **{f"D{i:02d}": False for i in range(1, 13)},
                **{f"S{i:02d}": True for i in range(1, 21)},
                **{f"C{i:02d}": False for i in range(1, 15)},
            },
            "fix_tiers": {"fix_immediately": False, "fix_and_report": False, "never_fix": False},
            "content_safety": {c["id"]: True for c in CONTENT_SAFETY},
            "realism_scoring": False,
        }
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
        f"Deep Stations ({len(enabled_deep)}/12):",
    ]
    for c in enabled_deep:
        lines.append(f"  [{c['id']}] {c['name']}")

    lines.append("")
    lines.append(f"Surface Scan ({len(enabled_surface)}/20):")
    for c in enabled_surface:
        lines.append(f"  [{c['id']}] {c['name']} -> {c['route']}")

    lines.append("")
    lines.append(f"Conditional ({len(enabled_conditional)}/14):")
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
