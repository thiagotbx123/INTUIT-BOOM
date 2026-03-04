# -*- coding: utf-8 -*-
"""NV2 Non-Profit Health Check — Demo Readiness Analyzer
Navega tela a tela em Parent, Rise e Response.
Extrai dados, valida contra expectativas NP, roda content scan.
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
ACCOUNTS["NV2_NP"] = {
    "name": "NV2 Non-Profit",
    "email": "quickbooks-np-tbxdemo@tbxofficial.com",
    "password": "TestBox!23",
    "totp_secret": "",  # Fill with actual TOTP secret
    "companies": {
        "parent": "Parent",
        "rise": "Rise",
        "response": "Response",
        "consolidated": "Consolidated",
    },
    "company_ids": {
        "parent": "",  # Fill with actual company IDs
        "rise": "",
        "response": "",
        "consolidated": "",
    },
    "default_company": "parent",
}

ENTITIES = [
    ("parent", "", "Parent (Main NP Org)"),
    ("rise", "", "Rise (Child Entity)"),
    ("response", "", "Response (Child Entity)"),
]

# NP Terminology mapping
NP_TERMS = {
    "customers": "Donors",
    "invoices": "Pledges",
    "products": "Programs",
    "projects": "Grants",
    "profit_and_loss": "Statement of Activity",
    "revenue": "Contributions & Grants",
    "cogs": "Program Expenses",
}

# Content scan patterns (subset — full list in content_scanner.py)
PROFANITY_PATTERNS = [
    r"\bdick(?:s|head|weed)?\b",
    r"\bfuck(?:ing|ed|er|s)?\b",
    r"\bshit(?:ty|s|head)?\b",
    r"\bass(?:hole|es|wipe)?\b",
    r"\bbitch(?:es|ing)?\b",
    r"\bbastard(?:s)?\b",
    r"\bcunt(?:s)?\b",
    r"\bwhore(?:s)?\b",
    r"\bslut(?:s)?\b",
    r"\bnigger(?:s)?\b",
    r"\bfaggot(?:s)?\b",
    r"\bretard(?:ed|s)?\b",
    r"\bmerda(?:s)?\b",
    r"\bporra(?:s)?\b",
    r"\bcaralho\b",
    r"\bputa(?:s)?\b",
    r"\bviado(?:s)?\b",
]

PLACEHOLDER_PATTERNS = [
    r"\btest\s*(?:123|456|789|data|user|account|company)\b",
    r"\bfoo(?:bar|baz)?\b",
    r"\bloremipsum\b",
    r"\basdf(?:ghjkl?)?\b",
    r"\bxxx+\b",
    r"\btodo\b",
    r"\bfixme\b",
    r"\bplaceholder\b",
    r"\bdummy\b",
    r"\bblah\b",
]

OUT = Path(r"C:\Users\adm_r\Downloads\NV2_HEALTH_CHECK_RESULT.json")


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
            if len(line) > 3 and any(
                w in line.lower() for w in ["parent", "rise", "response", "consolidated", "non-profit"]
            ):
                return line
    except Exception:
        pass
    return "?"


def switch(page, cid, name):
    """Switch entity via URL. Returns True/False."""
    if not cid:
        print(f"    SKIP: No company ID for {name}")
        return False
    url = f"https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={cid}"
    try:
        page.goto(url, timeout=60000)
        time.sleep(10)
        current = header_company(page)
        key_word = name.split()[0].lower()
        if key_word in current.lower():
            return True
        if is_in_qbo(page):
            return True
    except Exception as e:
        print(f"    SWITCH ERR: {e}")
    return False


def content_scan(text, location):
    """Run content scan on text. Returns list of violations."""
    violations = []

    for pattern in PROFANITY_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            violations.append(
                {
                    "severity": "CRITICAL",
                    "category": "profanity",
                    "text": match.group(),
                    "location": location,
                }
            )

    for pattern in PLACEHOLDER_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            violations.append(
                {
                    "severity": "MEDIUM",
                    "category": "placeholder",
                    "text": match.group(),
                    "location": location,
                }
            )

    return violations


# ── Page Analyzers ────────────────────────────────────────────
def check_dashboard(page, ek):
    """Dashboard /app/homepage — widgets, data, overall health."""
    go(page, "/app/homepage", wait=10)
    t = txt(page, timeout=8)
    d = {"page": "dashboard"}

    d["income"] = find_money(t, "Income") or find_money(t, "Contributions")
    d["expenses"] = find_money(t, "Expenses") or find_money(t, "Program Expenses")
    d["bank_accounts"] = find_money(t, "Bank accounts")
    d["ar"] = find_money(t, "Accounts receivable")
    d["ap"] = find_money(t, "Accounts payable")

    negs = find_all_negatives(t)
    d["negative_values"] = negs[:10] if negs else []

    findings = []
    if not d.get("income"):
        findings.append(("HIGH", "Contributions/Income NAO visivel no dashboard"))
    if d.get("bank_accounts") and d["bank_accounts"] < 0:
        findings.append(("CRITICAL", f"Bank balance NEGATIVO: ${d['bank_accounts']:,.0f}"))

    # Content scan
    violations = content_scan(t, f"{ek}/dashboard")
    if violations:
        for v in violations:
            findings.append((v["severity"], f"Content: '{v['text']}' ({v['category']})"))
    d["content_violations"] = violations

    d["findings"] = findings
    return d


def check_donors(page, ek):
    """Donors (Customers) /app/customers — count, names, content scan."""
    go(page, "/app/customers", wait=6)
    t = txt(page)
    d = {"page": "donors"}

    m = re.search(r"(\d+)\s*(?:customers?|donors?|results?)", t, re.IGNORECASE)
    d["count_text"] = m.group(0) if m else None

    findings = []
    test_names = re.findall(r"(?i)\b(test|delete|sample|dummy|xxx|fake)\b", t)
    if test_names:
        findings.append(("HIGH", f"Nomes de teste em donors: {set(test_names)}"))

    # Content scan
    violations = content_scan(t, f"{ek}/donors")
    if violations:
        for v in violations:
            findings.append((v["severity"], f"Content: '{v['text']}' ({v['category']})"))
    d["content_violations"] = violations

    d["findings"] = findings
    return d


def check_pledges(page, ek):
    """Pledges (Invoices) /app/invoices — totals, status mix."""
    go(page, "/app/invoices", wait=6)
    t = txt(page)
    d = {"page": "pledges"}
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
                findings.append(("HIGH", f"Pledges {overdue_pct:.0f}% overdue — NP nao cobra doadores?"))
    if not d.get("unpaid") and not d.get("paid"):
        findings.append(("CRITICAL", "Pagina de pledges VAZIA"))

    d["findings"] = findings
    return d


def check_dimensions(page, ek):
    """Dimensions Hub /app/class — active dimensions, values, content scan."""
    go(page, "/app/class", wait=6)
    t = txt(page)
    d = {"page": "dimensions"}

    # Check for dimension content
    d["has_data"] = len(t.strip()) > 100
    d["has_restriction"] = bool(re.search(r"restriction", t, re.IGNORECASE))

    # Count visible dimensions
    dim_keywords = ["class", "department", "location", "fund", "restriction"]
    found_dims = [kw for kw in dim_keywords if kw in t.lower()]
    d["dimensions_found"] = found_dims
    d["dimension_count"] = len(found_dims)

    findings = []
    if not d["has_data"]:
        findings.append(("CRITICAL", "Dimensions Hub VAZIO"))
    if not d["has_restriction"]:
        findings.append(("HIGH", "Restriction dimension NAO encontrada — NP-critical"))
    if d["dimension_count"] < 5:
        findings.append(("HIGH", f"Apenas {d['dimension_count']} dimensoes encontradas (esperado: 5)"))

    # Content scan on dimension values
    violations = content_scan(t, f"{ek}/dimensions")
    if violations:
        for v in violations:
            findings.append((v["severity"], f"Content: '{v['text']}' ({v['category']})"))
    d["content_violations"] = violations

    d["findings"] = findings
    return d


def check_multi_entity(page, ek):
    """Multi-entity — switcher shows all entities."""
    d = {"page": "multi_entity"}
    findings = []

    # Check header for company switcher
    try:
        h = page.locator("header").first.inner_text()
        d["header_text"] = h[:200]

        # Look for company name in header
        d["current_entity"] = header_company(page)
    except Exception as e:
        d["header_text"] = f"ERR: {e}"
        findings.append(("HIGH", f"Nao consegui ler header: {e}"))

    d["findings"] = findings
    return d


def check_statement_of_activity(page, ek):
    """Statement of Activity (P&L for NP) via /app/reportlist."""
    go(page, "/app/reportlist", wait=5)
    t = txt(page, timeout=3)

    d = {"page": "statement_of_activity"}
    d["has_report"] = bool(re.search(r"statement\s+of\s+activity", t, re.IGNORECASE))

    findings = []
    if not d["has_report"]:
        findings.append(("HIGH", "Statement of Activity NAO encontrado na lista de reports"))
        d["findings"] = findings
        return d

    # Try to click on it
    try:
        link = page.locator('a:has-text("Statement of Activity")').first
        if link.is_visible(timeout=5000):
            link.click()
            time.sleep(8)
            t = txt(page, timeout=5)

            d["contributions"] = find_money(t, "Contributions") or find_money(t, "Total Contributions")
            d["grants"] = find_money(t, "Grants") or find_money(t, "Total Grants")
            d["program_expenses"] = find_money(t, "Program Expenses") or find_money(t, "Total Expenses")
            d["net_assets"] = find_money(t, "Net Assets") or find_money(t, "Change in Net Assets")

            if d.get("net_assets") and d["net_assets"] < 0:
                findings.append(("CRITICAL", f"Net Assets NEGATIVO: ${d['net_assets']:,.0f}"))
            if not d.get("contributions") and not d.get("grants"):
                findings.append(("HIGH", "Contributions/Grants NAO visiveis no report"))
    except Exception as e:
        findings.append(("HIGH", f"Erro ao abrir Statement of Activity: {e}"))

    d["findings"] = findings
    d["raw_snippet"] = t[:1500] if t else ""
    return d


def check_vendors(page, ek):
    """Vendors — count, realistic names, content scan."""
    go(page, "/app/vendors", wait=6)
    t = txt(page)
    d = {"page": "vendors"}
    m = re.search(r"(\d+)\s*(?:vendors?|results?)", t, re.IGNORECASE)
    d["count_text"] = m.group(0) if m else None

    findings = []
    test_names = re.findall(r"(?i)\b(test|delete|sample|dummy|xxx|fake)\b", t)
    if test_names:
        findings.append(("HIGH", f"Nomes de teste em vendors: {set(test_names)}"))

    violations = content_scan(t, f"{ek}/vendors")
    if violations:
        for v in violations:
            findings.append((v["severity"], f"Content: '{v['text']}' ({v['category']})"))
    d["content_violations"] = violations

    d["findings"] = findings
    return d


def check_programs(page, ek):
    """Programs (Products) /app/items — names, content scan."""
    go(page, "/app/items", wait=6)
    t = txt(page)
    d = {"page": "programs"}

    findings = []
    if "no products" in t.lower() or "get started" in t.lower() or len(t.strip()) < 80:
        findings.append(("HIGH", "Programs VAZIO"))
        d["has_programs"] = False
    else:
        d["has_programs"] = True
        test_names = re.findall(r"(?i)\b(test|delete|sample|dummy|product_)\b", t)
        if test_names:
            findings.append(("HIGH", f"Programs com nomes de teste: {set(test_names)}"))

    violations = content_scan(t, f"{ek}/programs")
    if violations:
        for v in violations:
            findings.append((v["severity"], f"Content: '{v['text']}' ({v['category']})"))
    d["content_violations"] = violations

    d["findings"] = findings
    return d


def check_projects(page, ek):
    """Grants (Projects) /app/projects — names, P&L tracking."""
    go(page, "/app/projects", wait=6)
    t = txt(page)
    d = {"page": "grants"}

    findings = []
    if "no projects" in t.lower() or "get started" in t.lower() or len(t.strip()) < 80:
        findings.append(("HIGH", "Grants/Projects VAZIO"))
        d["has_projects"] = False
    else:
        d["has_projects"] = True
        test_names = re.findall(r"(?i)\b(test|delete|sample|dummy|project_)\b", t)
        if test_names:
            findings.append(("HIGH", f"Grants com nomes de teste: {set(test_names)}"))

    d["findings"] = findings
    return d


def check_coa_banking(page, ek):
    """COA + Banking — accounts, content scan, bank balances."""
    # COA
    go(page, "/app/chartofaccounts?jobId=accounting", wait=6)
    t_coa = txt(page)
    d = {"page": "coa_banking"}

    findings = []
    violations_coa = content_scan(t_coa, f"{ek}/coa")
    if violations_coa:
        for v in violations_coa:
            findings.append((v["severity"], f"COA Content: '{v['text']}' ({v['category']})"))

    # Banking
    go(page, "/app/banking", wait=6)
    t_bank = txt(page)
    balances = re.findall(r"-?\$[\d,]+\.?\d*", t_bank)
    d["bank_amounts"] = balances[:8] if balances else []

    neg_bank = [b for b in balances if b.startswith("-")]
    if neg_bank:
        findings.append(("CRITICAL", f"Saldos bancarios negativos: {neg_bank[:3]}"))
    if not balances:
        findings.append(("HIGH", "Banking sem saldos visiveis"))

    m = re.search(r"(?i)(?:for\s+review|categorize)\s*[\(:]?\s*(\d+)", t_bank)
    d["for_review"] = int(m.group(1)) if m else 0

    d["content_violations"] = violations_coa
    d["findings"] = findings
    return d


# ── Main ──────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  NV2 NON-PROFIT HEALTH CHECK — Demo Readiness")
    print("=" * 60)

    # Login
    try:
        pw, browser, page = start_round("NV2_NP", "parent")
    except Exception as e:
        print(f"  Login falhou: {e}")
        print("  Certifique-se de preencher credenciais em ACCOUNTS['NV2_NP']")
        return

    print(f"  Logado. Header: {header_company(page)}")

    results = {}
    checks = [
        check_dashboard,
        check_donors,
        check_pledges,
        check_dimensions,
        check_multi_entity,
        check_statement_of_activity,
        check_vendors,
        check_programs,
        check_projects,
        check_coa_banking,
    ]

    for ek, cid, name in ENTITIES:
        print(f"\n{'=' * 60}")
        print(f"  {name} ({ek})")
        print(f"{'=' * 60}")

        if cid and not switch(page, cid, name):
            print(f"  FALHA no switch para {name}! Tentando continuar...")
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
                n_content = len(result.get("content_violations", []))
                if n_findings:
                    print(f"  {n_findings} findings", end="")
                    if n_content:
                        print(f" ({n_content} content)", end="")
                    print()
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
    all_content_violations = []
    for ek, data in results.items():
        for pg, pg_data in data.get("pages", {}).items():
            for sev, msg in pg_data.get("findings", []):
                all_findings.append({"entity": ek, "page": pg, "severity": sev, "detail": msg})
            for v in pg_data.get("content_violations", []):
                all_content_violations.append({**v, "entity": ek})

    # Sort by severity
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_findings.sort(key=lambda x: sev_order.get(x["severity"], 99))

    # Print summary
    print(f"\n  TOTAL FINDINGS: {len(all_findings)}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        cnt = sum(1 for f in all_findings if f["severity"] == sev)
        if cnt:
            print(f"    {sev}: {cnt}")

    print(f"\n  CONTENT SCAN VIOLATIONS: {len(all_content_violations)}")
    for ek in ["parent", "rise", "response"]:
        entity_v = [v for v in all_content_violations if v.get("entity") == ek]
        if entity_v:
            print(f"    {ek}: {len(entity_v)} violations")
        else:
            print(f"    {ek}: CLEAN")

    print("\n  TOP FINDINGS:")
    for i, f in enumerate(all_findings[:15], 1):
        print(f"    {i}. [{f['severity']}] {f['entity']}/{f['page']}: {f['detail']}")

    # Realism score
    total_checks = len(checks) * len(ENTITIES)
    pass_count = total_checks - len([f for f in all_findings if f["severity"] in ("CRITICAL", "HIGH")])
    realism_score = max(0, min(10, round(pass_count / total_checks * 10, 1)))
    print(f"\n  REALISM SCORE: {realism_score}/10")

    # Save JSON
    output = {
        "date": __import__("datetime").datetime.now().isoformat(),
        "environment": "NV2 Non-Profit",
        "dataset_id": "3e1337cc-70ca-4041-bc95-0fe29181bb12",
        "results": results,
        "findings": all_findings,
        "content_violations": all_content_violations,
        "summary": {
            "total_findings": len(all_findings),
            "critical": sum(1 for f in all_findings if f["severity"] == "CRITICAL"),
            "high": sum(1 for f in all_findings if f["severity"] == "HIGH"),
            "content_violations": len(all_content_violations),
            "realism_score": realism_score,
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
    print("  NV2 HEALTH CHECK COMPLETO")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
