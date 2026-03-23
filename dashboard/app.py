"""QBO Demo Manager — FastAPI Web Dashboard."""

import sys
from pathlib import Path

# Ensure dashboard package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from actions import generate_sweep_prompt, sync_retool, test_login
from config import (
    get_account_config,
    load_profiles,
    save_account_config,
    save_profile,
)
from data import compute_sweep_delta, get_account, load_accounts, load_sweep_history
from sweep_checks import (
    CONDITIONAL_CHECKS,
    CONTENT_SAFETY,
    DEEP_STATIONS,
    DEMO_REALISM_CRITERIA,
    FIX_TIERS,
    SURFACE_SCAN,
)
from sweep_engine import generate_sweep_order_md
from logger import get_logger

log = get_logger("qbo_dashboard")

app = FastAPI(title="QBO Demo Manager")

BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE / "templates"))


# ─── Dashboard ───


def _get_active_sweep() -> dict | None:
    """Read LATEST_SWEEP.json and return data if status is pending/interrupted.

    Crash detection (3 methods):
    1. PID check — tasklist confirms process alive
    2. Timeout — sweep pending >3 hours with no progress update = likely crashed
    3. Progress stall — last_update in progress >90 min ago = likely hung
    """
    import json as json_mod
    from datetime import datetime, timedelta

    sweep_file = BASE / "pending" / "LATEST_SWEEP.json"
    if not sweep_file.exists():
        return None
    try:
        data = json_mod.loads(sweep_file.read_text(encoding="utf-8"))
        if data.get("status") == "pending":
            is_crashed = False
            crash_reason = ""

            # Method 1: PID check
            pid = data.get("pid")
            if pid:
                import subprocess as _sp

                try:
                    check = _sp.run(
                        ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    if str(pid) not in check.stdout:
                        is_crashed = True
                        crash_reason = f"PID {pid} not found"
                except (OSError, _sp.TimeoutExpired):
                    # tasklist itself failed — fall through to timeout check
                    pass

            # Method 2: Activation timeout (3 hours with no progress)
            if not is_crashed:
                activated_at = data.get("activated_at", "")
                progress = data.get("progress", {})
                last_update = progress.get("last_update", "")
                try:
                    act_time = datetime.fromisoformat(activated_at)
                    ref_time = datetime.fromisoformat(last_update) if last_update else act_time
                    if datetime.now() - ref_time > timedelta(hours=3):
                        is_crashed = True
                        crash_reason = f"No activity for 3+ hours (last: {ref_time.isoformat()})"
                except (ValueError, TypeError):
                    pass

            if is_crashed:
                data["status"] = "interrupted"
                data["interrupted_at"] = datetime.now().isoformat()
                data["interrupted_reason"] = crash_reason
                sweep_file.write_text(
                    json_mod.dumps(data, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                log.warning(
                    "Sweep interrupted: %s (account: %s)", crash_reason, data.get("account", {}).get("shortcode", "?")
                )

            return data
        if data.get("status") == "interrupted":
            return data
    except Exception as e:
        log.debug("Could not read active sweep state: %s", e)
    return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    accounts = load_accounts()
    total_entities = sum(len(a.companies) for a in accounts)
    active_sweep = _get_active_sweep()
    # Compute deltas for trend indicators in the table
    deltas = {}
    for acct in accounts:
        d = compute_sweep_delta(acct.shortcode)
        if d:
            deltas[acct.shortcode] = d
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "accounts": accounts,
            "total_entities": total_entities,
            "active_sweep": active_sweep,
            "deltas": deltas,
        },
    )


@app.get("/account/{shortcode}", response_class=HTMLResponse)
async def account_detail(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse(f"<h2>Account '{shortcode}' not found</h2>", status_code=404)
    history = load_sweep_history(shortcode)
    delta = compute_sweep_delta(shortcode)
    # Build sparkline data (only entries with health)
    sparkline = [{"date": e.date, "health": e.health} for e in history if e.health is not None]
    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "account": account,
            "history": history,
            "delta": delta,
            "sparkline": sparkline,
        },
    )


@app.get("/api/accounts/{shortcode}/history")
async def account_history(shortcode: str):
    """API: return sweep history + delta for an account."""
    history = load_sweep_history(shortcode)
    delta = compute_sweep_delta(shortcode)
    return {"history": [e.model_dump() for e in history], "delta": delta}


# ─── Config Panel ───


@app.get("/config", response_class=HTMLResponse)
async def config_panel(request: Request, profile: str = "", account: str = ""):
    accounts = load_accounts()
    profiles = load_profiles()

    # If account is specified and no explicit profile override, use account's saved profile
    acct_cfg = get_account_config(account) if account else {}
    if not profile and acct_cfg.get("profile") and acct_cfg["profile"] in profiles:
        active_profile = acct_cfg["profile"]
    else:
        active_profile = profile if profile and profile in profiles else "full_sweep"
    p = profiles[active_profile]

    return templates.TemplateResponse(
        "config.html",
        {
            "request": request,
            "accounts": accounts,
            "profiles": profiles,
            "active_profile": active_profile,
            "target_shortcode": account,
            "profile": p,
            "profile_checks": p.get("checks", {}),
            "profile_fix": p.get("fix_tiers", {}),
            "profile_safety": p.get("content_safety", {}),
            "deep_stations": DEEP_STATIONS,
            "surface_scan": SURFACE_SCAN,
            "conditional_checks": CONDITIONAL_CHECKS,
            "content_safety": CONTENT_SAFETY,
            "fix_tiers": FIX_TIERS,
            "realism_criteria": DEMO_REALISM_CRITERIA,
            "account_notes": acct_cfg.get("notes", ""),
        },
    )


# ─── Config API ───


@app.post("/api/config/save-profile")
async def api_save_profile(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=422)
    if "key" not in body or "profile" not in body:
        return JSONResponse({"error": "Missing required fields: key, profile"}, status_code=422)
    save_profile(body["key"], body["profile"])
    return JSONResponse({"status": "ok"})


@app.post("/api/config/save-account")
async def api_save_account(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=422)
    if "shortcode" not in body or "config" not in body:
        return JSONResponse({"error": "Missing required fields: shortcode, config"}, status_code=422)
    save_account_config(body["shortcode"], body["config"])
    return JSONResponse({"status": "ok"})


@app.post("/api/config/activate-sweep", response_class=HTMLResponse)
async def api_activate_sweep(request: Request, profile: str = "full_sweep", account: str = "", force: str = ""):
    """Save sweep config to pending file. Claude Code reads it on 'roda'."""
    import datetime
    import json as json_mod

    if not account:
        return HTMLResponse("<div class='error'>No account selected</div>", status_code=400)

    acct = get_account(account)
    if not acct:
        return HTMLResponse(f"<div class='error'>Account '{account}' not found</div>", status_code=404)

    # Save structured config (not just text prompt)
    pending_dir = BASE / "pending"
    pending_dir.mkdir(exist_ok=True)

    # --- SWEEP LOCK: prevent double activation ---
    latest_file = pending_dir / "LATEST_SWEEP.json"
    if latest_file.exists() and force != "1":
        try:
            existing = json_mod.loads(latest_file.read_text(encoding="utf-8"))
            if existing.get("status") == "pending" and existing.get("pid"):
                # Verify sweep process is actually running before blocking
                import subprocess as _sp

                check = _sp.run(
                    ["tasklist", "/FI", f"PID eq {existing['pid']}", "/NH"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if str(existing["pid"]) in check.stdout:
                    # Process alive — redirect to dashboard where banner shows status
                    from fastapi.responses import RedirectResponse

                    return RedirectResponse(url="/", status_code=303)
                # Process dead — stale lock, proceed with new sweep
        except (json_mod.JSONDecodeError, KeyError):
            pass  # corrupted file, proceed normally

    profiles = load_profiles()
    p = profiles.get(profile, profiles["full_sweep"])

    sweep_order = {
        "activated_at": datetime.datetime.now().isoformat(),
        "account": {
            "shortcode": acct.shortcode,
            "email": acct.email,
            "label": acct.label,
            "password": acct.password,
            "totp_secret": acct.totp_secret,
            "dataset": acct.dataset,
            "companies": [c.model_dump() for c in acct.companies],
        },
        "profile": profile,
        "profile_name": p["name"],
        "checks": p.get("checks", {}),
        "fix_tiers": p.get("fix_tiers", {}),
        "content_safety": p.get("content_safety", {}),
        "realism_scoring": p.get("realism_scoring", True),
        "notes": get_account_config(account).get("notes", ""),
        "status": "pending",
    }

    latest_file = pending_dir / "LATEST_SWEEP.json"
    latest_file.write_text(json_mod.dumps(sweep_order, indent=2, ensure_ascii=False), encoding="utf-8")

    # Build enabled check lists for SWEEP_ORDER generation
    checks = p.get("checks", {})
    deep = [s for s in DEEP_STATIONS if checks.get(s["id"], True)]
    surface = [s for s in SURFACE_SCAN if checks.get(s["id"], True)]
    cond = [s for s in CONDITIONAL_CHECKS if checks.get(s["id"], True)]

    # Generate SWEEP_ORDER.md — compact version (v6.0) with external references
    generate_sweep_order_md(pending_dir, acct, p, profile, deep, surface, cond)
    log.info(
        "Sweep activated: %s (%s) profile=%s deep=%d surface=%d cond=%d",
        acct.shortcode,
        acct.label,
        profile,
        len(deep),
        len(surface),
        len(cond),
    )

    # Launch Claude CLI in a new console window — autonomous execution
    import os
    import subprocess as sp

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)  # Allow spawning Claude from within Claude sessions

    safe_label = "".join(c for c in acct.label if c.isalnum() or c in " -_.")
    sweep_title = f"QBO Sweep - {safe_label}"

    bat_file = pending_dir / "run_sweep.bat"
    bat_file.write_text(
        f"@echo off\n"
        f"title {sweep_title}\n"
        f"cd /d {BASE.parent}\n"
        f'claude "Pending sweep detected. Read dashboard/pending/SWEEP_ORDER.md and execute it. Use ONLY the credentials in SWEEP_ORDER.md. Do NOT read PROMPT_CLAUDE_QBO_MASTER.md or TESTBOX_ACCOUNTS.md."'
        f" --dangerously-skip-permissions\n"
        f"echo.\n"
        f"echo === SWEEP FINALIZADO ===\n"
        f"pause\n",
        encoding="utf-8",
    )

    proc = sp.Popen(
        ["cmd", "/c", str(bat_file)],
        creationflags=sp.CREATE_NEW_CONSOLE,
        env=env,
    )

    sweep_order["pid"] = proc.pid
    sweep_order["window_title"] = sweep_title
    latest_file.write_text(json_mod.dumps(sweep_order, indent=2, ensure_ascii=False), encoding="utf-8")

    log.info("Sweep process launched: PID %d, window '%s'", proc.pid, sweep_title)

    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/", status_code=303)


@app.post("/api/config/stop-sweep", response_class=HTMLResponse)
async def api_stop_sweep():
    """Kill running Claude sweep process and reset LATEST_SWEEP.json status."""
    import json as json_mod
    import subprocess as sp

    pending_dir = BASE / "pending"
    latest_file = pending_dir / "LATEST_SWEEP.json"
    data = None

    if latest_file.exists():
        try:
            data = json_mod.loads(latest_file.read_text(encoding="utf-8"))
            data["status"] = "cancelled"
            data["cancelled_at"] = __import__("datetime").datetime.now().isoformat()
            latest_file.write_text(json_mod.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            log.info("Sweep cancelled: %s", data.get("account", {}).get("shortcode", "?"))
        except Exception:
            pass

    # Kill sweep process by PID
    pid = data.get("pid") if data else None
    if pid:
        try:
            sp.run(f"taskkill /F /PID {pid} /T", shell=True, capture_output=True, timeout=10)
        except Exception:
            pass

    # Fallback: kill any remaining QBO Sweep windows
    try:
        sp.run('taskkill /F /FI "WINDOWTITLE eq QBO Sweep*" /T', shell=True, capture_output=True, timeout=10)
    except Exception:
        pass

    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/", status_code=303)


@app.post("/api/config/resume-sweep", response_class=HTMLResponse)
async def api_resume_sweep():
    """Resume an interrupted sweep — regenerate SWEEP_ORDER with progress, spawn Claude."""
    import datetime
    import json as json_mod
    import os
    import subprocess as sp

    pending_dir = BASE / "pending"
    latest_file = pending_dir / "LATEST_SWEEP.json"

    if not latest_file.exists():
        return HTMLResponse("<div class='error'>No sweep to resume</div>", status_code=400)

    data = json_mod.loads(latest_file.read_text(encoding="utf-8"))
    if data.get("status") not in ("interrupted", "cancelled"):
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/", status_code=303)

    # Get account and profile
    acct_info = data.get("account", {})
    acct = get_account(acct_info.get("shortcode", ""))
    if not acct:
        return HTMLResponse("<div class='error'>Account not found</div>", status_code=404)

    profiles = load_profiles()
    profile_key = data.get("profile", "full_sweep")
    p = profiles.get(profile_key, profiles["full_sweep"])

    # Extract progress
    progress = data.get("progress", {})

    # Build enabled check lists
    checks = p.get("checks", {})
    deep = [s for s in DEEP_STATIONS if checks.get(s["id"], True)]
    surface = [s for s in SURFACE_SCAN if checks.get(s["id"], True)]
    cond = [s for s in CONDITIONAL_CHECKS if checks.get(s["id"], True)]

    # Regenerate SWEEP_ORDER.md with resume info
    generate_sweep_order_md(pending_dir, acct, p, profile_key, deep, surface, cond, resume_from=progress)

    # Update status back to pending
    data["status"] = "pending"
    data["resumed_at"] = datetime.datetime.now().isoformat()

    # Launch Claude CLI in new console window
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    safe_label = "".join(c for c in acct.label if c.isalnum() or c in " -_.")
    sweep_title = f"QBO Sweep - {safe_label}"

    bat_file = pending_dir / "run_sweep.bat"
    bat_file.write_text(
        f"@echo off\n"
        f"title {sweep_title}\n"
        f"cd /d {BASE.parent}\n"
        f'claude "Retomar sweep interrompido. Read dashboard/pending/SWEEP_ORDER.md and execute from where it left off. Use ONLY the credentials in SWEEP_ORDER.md."'
        f" --dangerously-skip-permissions\n"
        f"echo.\n"
        f"echo === SWEEP FINALIZADO ===\n"
        f"pause\n",
        encoding="utf-8",
    )

    proc = sp.Popen(
        ["cmd", "/c", str(bat_file)],
        creationflags=sp.CREATE_NEW_CONSOLE,
        env=env,
    )

    data["pid"] = proc.pid
    data["window_title"] = sweep_title
    latest_file.write_text(json_mod.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    log.info(
        "Sweep resumed: %s PID %d (progress: %d stations done)",
        acct.shortcode,
        proc.pid,
        len(progress.get("completed_stations", [])),
    )

    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/", status_code=303)


# ─── Action API ───


@app.post("/api/test-login/{shortcode}", response_class=HTMLResponse)
async def api_test_login(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse("<div class='error'>Account not found</div>", status_code=404)
    result = test_login(account)
    return templates.TemplateResponse(
        "partials/action_log.html",
        {
            "request": request,
            "action": "login",
            "result": result,
        },
    )


@app.post("/api/sweep/{shortcode}", response_class=HTMLResponse)
async def api_sweep(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse("<div class='error'>Account not found</div>", status_code=404)
    prompt = generate_sweep_prompt(account)
    return templates.TemplateResponse(
        "partials/action_log.html",
        {
            "request": request,
            "action": "sweep",
            "prompt": prompt,
        },
    )


@app.post("/api/sync-retool", response_class=HTMLResponse)
async def api_sync_retool(request: Request):
    result = sync_retool()
    return templates.TemplateResponse(
        "partials/action_log.html",
        {
            "request": request,
            "action": "retool",
            "result": result,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8082, reload=True)
