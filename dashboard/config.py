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
    """Load sweep profiles — God Complete v8.0 is the ONLY profile.

    No more full_sweep/quick_sweep/surface_only. One profile, all checks enabled.
    """
    profiles = _load_json(PROFILES_FILE, {})

    # Ensure god_complete exists with ALL checks enabled
    all_check_ids = {c["id"] for c in get_all_checks()}
    all_cs_ids = {c["id"] for c in CONTENT_SAFETY}
    all_rv_ids = {r["id"] for r in REVALIDATION_RULES}

    needs_regen = "god_complete" not in profiles
    if not needs_regen:
        # Check if any new checks are missing
        existing = set(profiles["god_complete"].get("checks", {}).keys())
        needs_regen = not all_check_ids.issubset(existing)

    if needs_regen:
        profiles = {
            "god_complete": {
                "name": "God Complete v8.0",
                "description": "UNICO profile. Todas 161+ checks habilitadas. Sem excecao.",
                "checks": {cid: True for cid in sorted(all_check_ids)},
                "fix_tiers": {"fix_immediately": True, "fix_and_report": True, "never_fix": False},
                "content_safety": {csid: True for csid in sorted(all_cs_ids)},
                "revalidation": {rid: True for rid in sorted(all_rv_ids)},
                "realism_scoring": True,
            }
        }
        _save_json(PROFILES_FILE, profiles)

    # Remove legacy profiles if they crept back in
    legacy = [k for k in profiles if k != "god_complete"]
    if legacy:
        for k in legacy:
            del profiles[k]
        _save_json(PROFILES_FILE, profiles)

    return profiles


def save_profile(key: str, profile: dict):
    """Save a sweep profile."""
    profiles = load_profiles()
    profiles[key] = profile
    _save_json(PROFILES_FILE, profiles)


def delete_profile(key: str):
    """Delete a sweep profile (god_complete cannot be deleted)."""
    if key == "god_complete":
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
            "profile": "god_complete",
            "overrides": {},
            "notes": "",
            "hidden": False,
        },
    )


# --- Prompt Generation ---


def generate_sweep_command(shortcode: str, account_label: str, account_email: str) -> str:
    """Generate the full sweep command based on account config."""
    cfg = get_account_config(shortcode)
    profile_key = cfg.get("profile", "god_complete")
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
