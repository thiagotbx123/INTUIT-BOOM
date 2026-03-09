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
from data import get_account, load_accounts
from sweep_checks import (
    CONDITIONAL_CHECKS,
    CONTENT_SAFETY,
    DEEP_STATIONS,
    DEMO_REALISM_CRITERIA,
    FIX_TIERS,
    SURFACE_SCAN,
)

app = FastAPI(title="QBO Demo Manager")

BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE / "templates"))


# ─── Dashboard ───


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    accounts = load_accounts()
    total_entities = sum(len(a.companies) for a in accounts)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "accounts": accounts,
            "total_entities": total_entities,
        },
    )


@app.get("/account/{shortcode}", response_class=HTMLResponse)
async def account_detail(request: Request, shortcode: str):
    account = get_account(shortcode)
    if not account:
        return HTMLResponse(f"<h2>Account '{shortcode}' not found</h2>", status_code=404)
    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "account": account,
        },
    )


# ─── Config Panel ───


@app.get("/config", response_class=HTMLResponse)
async def config_panel(request: Request, profile: str = "full_sweep", account: str = ""):
    accounts = load_accounts()
    profiles = load_profiles()

    active_profile = profile if profile in profiles else "full_sweep"
    p = profiles[active_profile]

    # Merge account config overrides
    acct_cfg = get_account_config(account) if account else {}
    if acct_cfg.get("profile") and acct_cfg["profile"] in profiles and not profile:
        active_profile = acct_cfg["profile"]
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
    body = await request.json()
    save_profile(body["key"], body["profile"])
    return JSONResponse({"status": "ok"})


@app.post("/api/config/save-account")
async def api_save_account(request: Request):
    body = await request.json()
    save_account_config(body["shortcode"], body["config"])
    return JSONResponse({"status": "ok"})


def _generate_sweep_order_md(pending_dir, acct, profile_data, profile_key, deep, surface, cond):
    """Generate a comprehensive SWEEP_ORDER.md the new Claude session can follow."""
    from sweep_checks import DEEP_STATIONS, SURFACE_SCAN, CONDITIONAL_CHECKS, CONTENT_SAFETY
    import datetime

    checks = profile_data.get("checks", {})
    fix = profile_data.get("fix_tiers", {})
    safety = profile_data.get("content_safety", {})

    # Build companies table
    companies_lines = []
    for c in acct.companies:
        companies_lines.append(f"| {c.name} | {c.cid} | {c.type} | {c.priority} |")

    # Build enabled deep checks
    deep_lines = []
    for s in DEEP_STATIONS:
        if checks.get(s["id"], True):
            items = ", ".join(s["what_to_check"][:3])
            fixes = ", ".join(s["fix_actions"][:2]) if s["fix_actions"] else "Report only"
            deep_lines.append(
                f"### {s['id']} — {s['name']}\n- **Route**: `{s['route']}`\n- **Check**: {items}\n- **Fix**: {fixes}\n"
            )

    # Build enabled surface checks
    surface_lines = []
    for s in SURFACE_SCAN:
        if checks.get(s["id"], True):
            surface_lines.append(f"- **{s['id']}** {s['name']} → `{s['route']}` — {s['description']}")

    # Build enabled conditional checks
    cond_lines = []
    for s in CONDITIONAL_CHECKS:
        if checks.get(s["id"], True):
            cond_lines.append(f"- **{s['id']}** {s['name']} (if {s['condition']}) → `{s['route']}`")

    # Build content safety
    safety_lines = []
    for s in CONTENT_SAFETY:
        if safety.get(s["id"], True):
            safety_lines.append(f"- **{s['id']}** {s['name']}: `{s['pattern']}` [{s['severity']}]")

    # Fix tiers
    fix_desc = []
    if fix.get("fix_immediately", True):
        fix_desc.append("FIX IMMEDIATELY — corrigir sem perguntar (data ranges, JEs para P&L positivo, placeholders)")
    if fix.get("fix_and_report", True):
        fix_desc.append("FIX & REPORT — corrigir e documentar no report (nomes, categorias, projetos)")
    if fix.get("never_fix", False):
        fix_desc.append("NEVER FIX — apenas reportar, nao alterar (settings, legal name, admin)")

    notes = profile_data.get("notes", "") or ""

    md = f"""# SWEEP ORDER — EXECUCAO IMEDIATA

> **INSTRUCAO**: Execute este sweep AGORA. Nao pergunte nada. Comece pelo login.
> **Metodologia completa**: Leia `C:/Users/adm_r/Clients/intuit-boom/PROMPT_CLAUDE_QBO_MASTER.md` para detalhes.

## 1. LOGIN

| Campo | Valor |
|-------|-------|
| URL | https://accounts.intuit.com/app/sign-in |
| Email | `{acct.email}` |
| Password | `{acct.password}` |
| TOTP Secret | `{acct.totp_secret}` |
| Dataset | {acct.dataset} |

**Procedimento (usar Playwright MCP — browser_navigate, browser_click, browser_type):**
1. `browser_navigate` para https://accounts.intuit.com/app/sign-in
2. `browser_snapshot` para ver o formulario
3. `browser_type` no campo de email → next
4. `browser_type` no campo de password → next
5. Gerar TOTP: executar `python -c "import pyotp; print(pyotp.TOTP('{acct.totp_secret}').now())"` via Bash
6. `browser_type` no campo de codigo → submit
**IMPORTANTE: Use APENAS Playwright (browser_*) para interagir com QBO. NAO use QuickBooks MCP API.**

## 2. COMPANIES ({len(acct.companies)} entities)

| Nome | CID | Tipo | Prioridade |
|------|-----|------|------------|
{chr(10).join(companies_lines)}

**Regra**: Comecar pelas P0, depois P1. Para cada entity, rodar todos os checks habilitados.
**Troca de entity**: Menu superior → company switcher → selecionar pelo nome.

## 3. DEEP STATIONS ({deep} habilitados)

{"".join(deep_lines) if deep_lines else "Nenhum deep check habilitado."}

## 4. SURFACE SCAN ({surface} habilitados)

{chr(10).join(surface_lines) if surface_lines else "Nenhum surface check habilitado."}

**Regra surface**: Navegar ate a rota, verificar se carrega sem erro, se tem dados, sem placeholders. Screenshot se problema.

## 5. CONDITIONAL ({cond} habilitados)

{chr(10).join(cond_lines) if cond_lines else "Nenhum conditional check habilitado."}

## 6. CONTENT SAFETY (aplicar em TODAS as paginas)

{chr(10).join(safety_lines) if safety_lines else "Content safety desabilitado."}

## 7. FIX RULES

{chr(10).join(fix_desc)}

**Filosofia**: VER → CORRIGIR → AVANCAR. Nao parar para reportar, corrigir inline.

## 8. REALISM SCORING

{"HABILITADO — ao final do sweep, pontuar 10 criterios de 1-10." if profile_data.get("realism_scoring", True) else "DESABILITADO"}

## 9. OUTPUT

Salvar report em: `C:/Users/adm_r/Clients/intuit-boom/knowledge-base/sweep-learnings/{acct.shortcode}_YYYY-MM-DD.md`

Formato do report:
```
# Sweep Report: {acct.label}
**Date**: YYYY-MM-DD
**Overall Score**: X/10
**Profile**: {profile_data.get("name", profile_key)}

## Entities Audited
(tabela com score por entity)

## Findings
(P0/P1/P2 com descricao e acao tomada)

## Realism Score
(10 criterios se habilitado)
```

{f"## 10. NOTAS{chr(10)}{chr(10)}{notes}" if notes else ""}

---
*Gerado em {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} pelo QBO Demo Manager Dashboard*
"""

    order_file = pending_dir / "SWEEP_ORDER.md"
    order_file.write_text(md.strip(), encoding="utf-8")


@app.post("/api/config/activate-sweep", response_class=HTMLResponse)
async def api_activate_sweep(request: Request, profile: str = "full_sweep", account: str = ""):
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

    # Count enabled checks
    deep = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("D") and v)
    surface = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("S") and v)
    cond = sum(1 for k, v in p.get("checks", {}).items() if k.startswith("C") and v)
    entities = len(acct.companies)

    # Generate SWEEP_ORDER.md — comprehensive instructions for new Claude session
    _generate_sweep_order_md(pending_dir, acct, p, profile, deep, surface, cond)

    # Launch Claude — CLAUDE.md protocol will detect the pending sweep and execute
    import os
    import subprocess as sp

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    sp.Popen(
        ["claude", "go"],
        cwd=r"C:\Users\adm_r\Clients\intuit-boom",
        env=env,
        creationflags=sp.CREATE_NEW_CONSOLE,
    )

    html = f"""
    <div class="generated-prompt">
        <div style="padding: 16px; background: #23863633; border: 1px solid var(--green); border-radius: 8px;">
            <div style="font-size: 16px; font-weight: 700; color: var(--green); margin-bottom: 8px;">
                SWEEP LAUNCHED
            </div>
            <div style="font-size: 13px; margin-bottom: 12px;">
                <strong>{acct.label}</strong> — {acct.email}
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px;">
                <div style="text-align: center; padding: 8px; background: var(--bg); border-radius: 4px;">
                    <div style="font-size: 20px; font-weight: 700; color: var(--blue);">{deep}</div>
                    <div style="font-size: 10px; color: var(--text-dim);">DEEP</div>
                </div>
                <div style="text-align: center; padding: 8px; background: var(--bg); border-radius: 4px;">
                    <div style="font-size: 20px; font-weight: 700; color: var(--blue);">{surface}</div>
                    <div style="font-size: 10px; color: var(--text-dim);">SURFACE</div>
                </div>
                <div style="text-align: center; padding: 8px; background: var(--bg); border-radius: 4px;">
                    <div style="font-size: 20px; font-weight: 700; color: var(--blue);">{cond}</div>
                    <div style="font-size: 10px; color: var(--text-dim);">COND.</div>
                </div>
                <div style="text-align: center; padding: 8px; background: var(--bg); border-radius: 4px;">
                    <div style="font-size: 20px; font-weight: 700; color: var(--blue);">{entities}</div>
                    <div style="font-size: 10px; color: var(--text-dim);">ENTITIES</div>
                </div>
            </div>
            <div style="padding: 10px; background: var(--bg); border-radius: 4px; font-size: 13px; text-align: center; color: var(--green);">
                Claude Code abriu em um novo terminal. Acompanhe o progresso lá.
            </div>
        </div>
    </div>
    """
    return HTMLResponse(html)


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

    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
