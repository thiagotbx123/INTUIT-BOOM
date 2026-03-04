# -*- coding: utf-8 -*-
"""TCO Health Check — Atlanta Demo Readiness
Navega tela a tela em Apex, Global Tread e RoadReady.
Extrai numeros, analisa contra benchmarks tire shop, propoe correcoes.
Sem screenshots — foco em eficiencia e output acionavel.
"""

import sys
import re
import time
import json

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))

from pathlib import Path
from qbo_checker.login import start_round, is_in_qbo, ACCOUNTS

# ── Config ────────────────────────────────────────────────────
ACCOUNTS["TCO_DEMO"] = {
    "name": "TCO DEMO",
    "email": "quickbooks-tco-tbxdemo@tbxofficial.com",
    "password": "TestBox!23",
    "totp_secret": "UGGQO4EAKKZTOK7XVXGOXHLUYZHBDXV7",
    "companies": {
        "apex": "Apex Tire",
        "global": "Global",
        "traction": "Traction Control Outfitters, LLC",
        "roadready": "RoadReady",
        "consolidated": "Vista consolidada",
    },
    "company_ids": {
        "apex": "9341455130166501",
        "global": "9341455130196737",
        "traction": "9341455130188547",
        "roadready": "9341455130170608",
        "consolidated": "9341455649090852",
    },
    "default_company": "apex",
}

ENTITIES = [
    ("apex", "9341455130166501", "Apex Tire & Auto Retail"),
    ("global", "9341455130196737", "Global Tread Distributors"),
    ("roadready", "9341455130170608", "RoadReady Service Solutions"),
]

OUT = Path(r"C:\Users\adm_r\Downloads\TCO_HEALTH_CHECK_RESULT.json")


# ── Helpers ───────────────────────────────────────────────────
def txt(page, timeout=3):
    """Get page body text, wait for load."""
    for _ in range(timeout):
        try:
            loading = page.locator('[class*="loading"], [class*="spinner"], [class*="Spinner"]').count()
            if loading == 0:
                break
        except Exception:
            pass
        time.sleep(1)
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def go(page, path, wait=6):
    """Navigate and wait."""
    try:
        page.goto(f"https://qbo.intuit.com{path}", timeout=30000)
        time.sleep(wait)
    except Exception as e:
        print(f"    NAV ERR {path}: {e}")


def money(s):
    """Parse dollar amount from text like '$1,234,567.89' or '-$500'."""
    if not s:
        return None
    s = s.replace(",", "").replace("$", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def find_money(text, label):
    """Find a dollar amount next to a label."""
    patterns = [
        rf"{label}\s*[\n\r]*\s*(-?\$[\d,]+\.?\d*)",
        rf"{label}\s*(-?\$[\d,]+\.?\d*)",
        rf"{label}[^\n$]*?(\$[\d,]+\.?\d*)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return money(m.group(1))
    return None


def find_all_negatives(text):
    """Find all negative dollar amounts visible."""
    return re.findall(r"-\$[\d,]+\.?\d*", text)


def header_company(page):
    """Read company name from Enterprise Suite header bar."""
    try:
        h = page.locator("header").first.inner_text()
        for line in h.split("\n"):
            line = line.strip()
            if len(line) > 5 and any(w in line for w in ["LLC", "Tire", "Tread", "Road", "Traction", "Consolidated"]):
                return line
    except Exception:
        pass
    return "?"


def switch(page, cid, name):
    """Switch entity via URL. Returns True/False."""
    url = f"https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={cid}"
    try:
        page.goto(url, timeout=60000)
        time.sleep(10)
        current = header_company(page)
        key_word = name.split()[0].lower()
        if key_word in current.lower():
            return True
        # might still work even if header reading fails
        if is_in_qbo(page):
            return True  # proceed with caution
    except Exception as e:
        print(f"    SWITCH ERR: {e}")
    return False


# ── Page Analyzers ────────────────────────────────────────────
def check_dashboard(page, ek):
    """Dashboard /app/homepage — KPIs, negatives, overall health."""
    go(page, "/app/homepage", wait=10)
    t = txt(page, timeout=8)
    d = {"page": "dashboard"}

    # Key metrics
    d["income"] = find_money(t, "Income")
    d["profit_loss"] = find_money(t, "Profit & loss") or find_money(t, "Profit and loss")
    d["bank_accounts"] = find_money(t, "Bank accounts")
    d["expenses"] = find_money(t, "Expenses")
    d["ar"] = find_money(t, "Accounts receivable")
    d["ap"] = find_money(t, "Accounts payable")
    d["sales"] = find_money(t, "Sales")
    d["invoices_unpaid"] = find_money(t, "Unpaid")
    d["invoices_overdue"] = find_money(t, "Overdue")

    # Negatives check
    negs = find_all_negatives(t)
    d["negative_values"] = negs[:10] if negs else []

    # Quick findings
    findings = []
    if d.get("profit_loss") and d["profit_loss"] < 0:
        findings.append(("CRITICAL", f"P&L NEGATIVO no dashboard: ${d['profit_loss']:,.0f}"))
    if d.get("bank_accounts") and d["bank_accounts"] < 0:
        findings.append(("CRITICAL", f"Bank balance NEGATIVO: ${d['bank_accounts']:,.0f}"))
    if negs:
        big_negs = [n for n in negs if money(n) and abs(money(n)) > 100000]
        if big_negs:
            findings.append(("HIGH", f"Valores negativos grandes visiveis: {big_negs[:3]}"))
    if not d.get("income"):
        findings.append(("CRITICAL", "Income NAO visivel no dashboard"))

    d["findings"] = findings
    return d


def check_pnl(page, ek):
    """P&L Report — revenue, COGS, expenses, net income."""
    # Try direct URLs first, then sidebar
    for path in ["/app/reports/profitandloss", "/app/report/profitandloss"]:
        go(page, path, wait=5)
        t = txt(page, timeout=3)
        if "sorry" not in t.lower() and "can't find" not in t.lower() and len(t) > 200:
            break
    else:
        # Sidebar fallback
        go(page, "/app/homepage", wait=3)
        try:
            r = page.locator('a:has-text("Reports")').first
            if r.is_visible(timeout=3000):
                r.click()
                time.sleep(3)
                pl = page.locator('a:has-text("Profit and Loss"), a:has-text("Profit & Loss")').first
                if pl.is_visible(timeout=5000):
                    pl.click()
                    time.sleep(8)
        except Exception:
            pass
        t = txt(page, timeout=5)

    d = {"page": "pnl"}
    d["total_income"] = find_money(t, "Total Income") or find_money(t, "Gross Income")
    d["cogs"] = find_money(t, "Cost of Goods Sold") or find_money(t, "Total COGS")
    d["gross_profit"] = find_money(t, "Gross Profit")
    d["total_expenses"] = find_money(t, "Total Expenses")
    d["net_income"] = find_money(t, "Net Income") or find_money(t, "Net Operating Income")
    d["payroll"] = find_money(t, "Payroll")

    findings = []
    if d.get("net_income") and d["net_income"] < 0:
        findings.append(("CRITICAL", f"Net Income NEGATIVO: ${d['net_income']:,.0f}"))
    if d.get("total_income") and d.get("cogs"):
        cogs_pct = d["cogs"] / d["total_income"] * 100
        d["cogs_pct"] = round(cogs_pct, 1)
        if cogs_pct < 30:
            findings.append(
                (
                    "HIGH",
                    f"COGS muito baixo ({cogs_pct:.0f}%) — tire shop deveria ser 50-70%",
                )
            )
        elif cogs_pct > 85:
            findings.append(
                (
                    "CRITICAL",
                    f"COGS absurdamente alto ({cogs_pct:.0f}%) — margem bruta negativa",
                )
            )
    if d.get("total_income") and not d.get("payroll"):
        findings.append(("HIGH", "Payroll NAO aparece no P&L — 250 employees sem salario?"))
    if "sorry" in t.lower() or "can't find" in t.lower():
        findings.append(("CRITICAL", "P&L report retorna 404"))
    if len(t.strip()) < 100:
        findings.append(("CRITICAL", "P&L report VAZIO"))

    d["findings"] = findings
    d["raw_snippet"] = t[:1500]
    return d


def check_balance_sheet(page, ek):
    """Balance Sheet — assets=liabilities+equity, cash, AR, AP."""
    for path in ["/app/reports/balancesheet", "/app/report/balancesheet"]:
        go(page, path, wait=5)
        t = txt(page, timeout=3)
        if "sorry" not in t.lower() and "can't find" not in t.lower() and len(t) > 200:
            break
    else:
        go(page, "/app/homepage", wait=3)
        try:
            r = page.locator('a:has-text("Reports")').first
            if r.is_visible(timeout=3000):
                r.click()
                time.sleep(3)
                bs = page.locator('a:has-text("Balance Sheet")').first
                if bs.is_visible(timeout=5000):
                    bs.click()
                    time.sleep(8)
        except Exception:
            pass
        t = txt(page, timeout=5)

    d = {"page": "balance_sheet"}
    d["total_assets"] = find_money(t, "TOTAL ASSETS") or find_money(t, "Total Assets")
    d["total_liabilities"] = find_money(t, "TOTAL LIABILITIES") or find_money(t, "Total Liabilities")
    d["total_equity"] = find_money(t, "Total Equity")
    d["cash"] = find_money(t, "Cash")
    d["ar"] = find_money(t, "Accounts Receivable")
    d["inventory"] = find_money(t, "Inventory")
    d["ap"] = find_money(t, "Accounts Payable")

    findings = []
    if "sorry" in t.lower() or "can't find" in t.lower():
        findings.append(("CRITICAL", "Balance Sheet retorna 404"))
    if d.get("total_assets") and d.get("cash") and d["cash"] < 0:
        findings.append(("CRITICAL", f"Cash NEGATIVO no BS: ${d['cash']:,.0f}"))

    d["findings"] = findings
    d["raw_snippet"] = t[:1500]
    return d


def check_customers(page, ek):
    """Customers — count, duplicates, test names."""
    go(page, "/app/customers", wait=6)
    t = txt(page)
    d = {"page": "customers"}

    # Count
    m = re.search(r"(\d+)\s*(?:customers?|results?)", t, re.IGNORECASE)
    d["count_text"] = m.group(0) if m else None

    findings = []
    test_names = re.findall(r"(?i)\b(test|delete|sample|dummy|xxx|fake)\b", t)
    if test_names:
        findings.append(("HIGH", f"Nomes de teste em customers: {set(test_names)}"))
    # Check for "2" suffix duplicates
    dupes = re.findall(r"\w+2\b", t)
    if len(dupes) > 3:
        findings.append(
            (
                "MEDIUM",
                f"Possiveis duplicatas (nomes com '2'): {len(dupes)} encontrados",
            )
        )

    d["findings"] = findings
    return d


def check_vendors(page, ek):
    """Vendors — count, realistic names."""
    go(page, "/app/vendors", wait=6)
    t = txt(page)
    d = {"page": "vendors"}
    m = re.search(r"(\d+)\s*(?:vendors?|results?)", t, re.IGNORECASE)
    d["count_text"] = m.group(0) if m else None
    d["findings"] = []
    return d


def check_invoices(page, ek):
    """Invoices — totals, overdue ratio."""
    go(page, "/app/invoices", wait=6)
    t = txt(page)
    d = {"page": "invoices"}
    d["unpaid"] = find_money(t, "Unpaid")
    d["overdue"] = find_money(t, "Overdue")
    d["paid"] = find_money(t, "Paid")
    d["deposited"] = find_money(t, "Deposited")

    findings = []
    if d.get("unpaid") and d.get("overdue"):
        if d["unpaid"] > 0:
            overdue_pct = d["overdue"] / d["unpaid"] * 100
            d["overdue_pct"] = round(overdue_pct, 1)
            if overdue_pct > 80:
                findings.append(
                    (
                        "HIGH",
                        f"AR {overdue_pct:.0f}% overdue — empresa nao cobra ninguem?",
                    )
                )
    if not d.get("unpaid") and not d.get("paid"):
        findings.append(("CRITICAL", "Pagina de invoices VAZIA"))

    d["findings"] = findings
    return d


def check_bills(page, ek):
    """Bills — totals, AP status."""
    go(page, "/app/bills", wait=6)
    t = txt(page)
    d = {"page": "bills"}
    d["open"] = find_money(t, "Open")
    d["overdue"] = find_money(t, "Overdue")
    d["paid"] = find_money(t, "Paid")

    findings = []
    if "no bills" in t.lower() or len(t.strip()) < 80:
        findings.append(("HIGH", "Pagina de bills VAZIA"))
    d["findings"] = findings
    return d


def check_banking(page, ek):
    """Banking — connected accounts, balances."""
    go(page, "/app/banking", wait=6)
    t = txt(page)
    d = {"page": "banking"}
    balances = re.findall(r"-?\$[\d,]+\.?\d*", t)
    d["visible_amounts"] = balances[:8] if balances else []

    # For Review count
    m = re.search(r"(?i)(?:for\s+review|categorize)\s*[\(:]?\s*(\d+)", t)
    d["for_review"] = int(m.group(1)) if m else 0

    findings = []
    neg_bank = [b for b in balances if b.startswith("-")]
    if neg_bank:
        findings.append(("CRITICAL", f"Saldos bancarios negativos: {neg_bank[:3]}"))
    if d["for_review"] > 50:
        findings.append(
            (
                "MEDIUM",
                f"{d['for_review']} transacoes 'For Review' — banking parece desorganizado",
            )
        )
    if not balances:
        findings.append(("HIGH", "Banking sem saldos visiveis — nao conectado?"))
    d["findings"] = findings
    return d


def check_payroll(page, ek):
    """Payroll — configured? employees? last run?"""
    go(page, "/app/payroll", wait=6)
    t = txt(page)
    d = {"page": "payroll"}

    findings = []
    setup_words = [
        "set up",
        "get started",
        "subscribe",
        "turn on",
        "enable",
        "not available",
    ]
    if any(w in t.lower() for w in setup_words):
        findings.append(("HIGH", "Payroll NAO configurado — apenas setup wizard"))
        d["status"] = "not_configured"
    elif "employees" in t.lower() or "payroll" in t.lower():
        d["status"] = "configured"
    else:
        d["status"] = "unknown"

    d["findings"] = findings
    return d


def check_projects(page, ek):
    """Projects — has data? names realistic?"""
    go(page, "/app/projects", wait=6)
    t = txt(page)
    d = {"page": "projects"}

    findings = []
    if "no projects" in t.lower() or "get started" in t.lower() or len(t.strip()) < 80:
        findings.append(("HIGH", "Projects VAZIO — feature aparece sem uso"))
        d["has_projects"] = False
    else:
        d["has_projects"] = True
        test_names = re.findall(r"(?i)\b(test|delete|sample|dummy)\b", t)
        if test_names:
            findings.append(("HIGH", f"Projects com nomes de teste: {set(test_names)}"))

    d["findings"] = findings
    return d


# ── Main ──────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  TCO HEALTH CHECK — Atlanta Demo Readiness")
    print("=" * 60)

    # Login
    try:
        pw, browser, page = start_round("TCO_DEMO", "apex")
    except Exception as e1:
        print(f"  TCO_DEMO falhou: {e1}, tentando TCO...")
        pw, browser, page = start_round("TCO", "apex")

    print(f"  Logado. Header: {header_company(page)}")

    results = {}
    checks = [
        check_dashboard,
        check_pnl,
        check_balance_sheet,
        check_customers,
        check_vendors,
        check_invoices,
        check_bills,
        check_banking,
        check_payroll,
        check_projects,
    ]

    for ek, cid, name in ENTITIES:
        print(f"\n{'=' * 60}")
        print(f"  {name} ({ek})")
        print(f"{'=' * 60}")

        if not switch(page, cid, name):
            print(f"  FALHA no switch para {name}! Tentando continuar...")
            # Navigate to homepage and check
            go(page, "/app/homepage", wait=5)

        current = header_company(page)
        print(f"  Header: {current}")

        entity_data = {"entity": name, "header": current, "pages": {}}

        for check_fn in checks:
            page_name = check_fn.__name__.replace("check_", "")
            print(f"  [{page_name}]", end=" ", flush=True)
            try:
                result = check_fn(page, ek)
                entity_data["pages"][page_name] = result
                n_findings = len(result.get("findings", []))
                if n_findings:
                    print(f"⚠ {n_findings} findings")
                    for sev, msg in result["findings"]:
                        print(f"    [{sev}] {msg}")
                else:
                    print("OK")
            except Exception as e:
                print(f"ERR: {e}")
                entity_data["pages"][page_name] = {
                    "error": str(e),
                    "findings": [("CRITICAL", f"Crash: {e}")],
                }

        results[ek] = entity_data

    # ── Compile & Output ──────────────────────────────────────
    print(f"\n{'=' * 60}")
    print("  COMPILANDO RESULTADOS")
    print(f"{'=' * 60}")

    all_findings = []
    for ek, data in results.items():
        for pg, pg_data in data.get("pages", {}).items():
            for sev, msg in pg_data.get("findings", []):
                all_findings.append({"entity": ek, "page": pg, "severity": sev, "detail": msg})

    # Sort by severity
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_findings.sort(key=lambda x: sev_order.get(x["severity"], 99))

    # Print summary
    print(f"\n  TOTAL FINDINGS: {len(all_findings)}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        cnt = sum(1 for f in all_findings if f["severity"] == sev)
        if cnt:
            print(f"    {sev}: {cnt}")

    print("\n  TOP FINDINGS:")
    for i, f in enumerate(all_findings[:15], 1):
        print(f"    {i}. [{f['severity']}] {f['entity']}/{f['page']}: {f['detail']}")

    # Per-entity financial summary
    print("\n  FINANCIAL SUMMARY:")
    for ek, data in results.items():
        dash = data["pages"].get("dashboard", {})
        pnl = data["pages"].get("pnl", {})
        print(f"\n  {data['entity']}:")
        print(f"    Dashboard Income: {dash.get('income')}")
        print(f"    Dashboard P&L: {dash.get('profit_loss')}")
        print(f"    Dashboard Bank: {dash.get('bank_accounts')}")
        print(f"    P&L Net Income: {pnl.get('net_income')}")
        print(f"    P&L COGS%: {pnl.get('cogs_pct', 'N/A')}")
        print(f"    Payroll on P&L: {pnl.get('payroll', 'NOT FOUND')}")
        print(f"    Negatives visible: {dash.get('negative_values', [])}")

    # Save JSON
    output = {
        "date": __import__("datetime").datetime.now().isoformat(),
        "results": results,
        "findings": all_findings,
        "summary": {
            "total": len(all_findings),
            "critical": sum(1 for f in all_findings if f["severity"] == "CRITICAL"),
            "high": sum(1 for f in all_findings if f["severity"] == "HIGH"),
        },
    }
    # Clean raw snippets for JSON
    for ek in output["results"]:
        for pg in output["results"][ek].get("pages", {}).values():
            pg.pop("raw_snippet", None)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  JSON salvo: {OUT}")

    try:
        pw.stop()
    except Exception:
        pass

    print(f"\n{'=' * 60}")
    print("  HEALTH CHECK COMPLETO")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
