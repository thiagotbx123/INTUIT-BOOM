# -*- coding: utf-8 -*-
"""
WFS EXPLORER - Navegacao Autonoma QBO + Mineral
================================================
Script para exploracao automatizada dos sistemas QBO e Mineral.

Uso:
    python wfs_explorer.py [comando]

Comandos:
    explore_qbo      - Explorar todas as rotas QBO
    explore_mineral  - Explorar Mineral HR
    health_check     - Verificar saude dos sistemas
    capture_all      - Capturar screenshots de tudo
"""

import time
import json
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

# ============================================================
# CONFIGURACAO
# ============================================================

CDP_PORT = 9222
OUTPUT_DIR = "wfs_mapping"

# Rotas QBO principais
QBO_ROUTES = {
    "core": [
        "/app/homepage",
        "/app/banking",
        "/app/customers",
        "/app/vendors",
        "/app/invoices",
        "/app/expenses",
        "/app/bills",
        "/app/reportlist",
        "/app/chartofaccounts",
        "/app/settings",
    ],
    "wfs": [
        "/app/payroll",
        "/app/payroll/overview",
        "/app/payroll/employees",
        "/app/payroll/contractors",
        "/app/payroll/taxes",
        "/app/employees",
        "/app/employees/list",
        "/app/employees/directory",
        "/app/employees/orgchart",
        "/app/timetracking",
        "/app/time",
        "/app/timesheets",
        "/app/projects",
        "/app/hr",
    ],
}

# Rotas Mineral
MINERAL_ROUTES = [
    "/dashboard",
    "/hr-compliance",
    "/company-policies",
    "/safety",
    "/training",
    "/hr-tools",
    "/templates",
    "/resources",
    "/my-cases",
    "/todo",
]

# ============================================================
# FUNCOES DE CONEXAO
# ============================================================


def connect_browser():
    """Conecta ao Chrome via CDP."""
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        return pw, browser, context, page
    except Exception as e:
        pw.stop()
        raise ConnectionError(f"Erro ao conectar: {e}")


def get_qbo_page(context):
    """Retorna a pagina do QBO."""
    for page in context.pages:
        if "qbo.intuit.com" in page.url:
            return page
    return context.pages[0]


def get_mineral_page(context):
    """Retorna a pagina do Mineral."""
    for page in context.pages:
        if "trustmineral.com" in page.url:
            return page
    return None


# ============================================================
# FUNCOES DE NAVEGACAO
# ============================================================


def navigate_qbo(page, route, timeout=30000):
    """Navega para uma rota do QBO."""
    url = f"https://qbo.intuit.com{route}"
    try:
        page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        time.sleep(2)
        return {"status": "OK", "url": page.url, "title": page.title()}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)[:100]}


def navigate_mineral(page, route, timeout=30000):
    """Navega para uma rota do Mineral."""
    url = f"https://apps.trustmineral.com{route}"
    try:
        page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        time.sleep(2)
        return {"status": "OK", "url": page.url, "title": page.title()}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)[:100]}


def open_mineral_from_qbo(qbo_page, context):
    """Abre o Mineral a partir do QBO."""
    # Ir para HR Advisor
    navigate_qbo(qbo_page, "/app/hr")
    time.sleep(3)

    # Clicar em "Go to Mineral"
    try:
        qbo_page.locator("text=Go to Mineral").click()
        time.sleep(5)

        # Retornar a pagina do Mineral
        return get_mineral_page(context)
    except Exception as e:
        print(f"Erro ao abrir Mineral: {e}")
        return None


# ============================================================
# FUNCOES DE EXPLORACAO
# ============================================================


def extract_page_data(page):
    """Extrai dados de uma pagina."""
    return page.evaluate(
        """() => {
        const data = {
            url: window.location.href,
            title: document.title,
            links: [],
            buttons: [],
            forms: []
        };

        // Links
        document.querySelectorAll('a[href]').forEach(a => {
            if (a.innerText.trim()) {
                data.links.push({
                    text: a.innerText.trim().substring(0, 50),
                    href: a.href
                });
            }
        });

        // Buttons
        document.querySelectorAll('button').forEach(b => {
            if (b.innerText.trim()) {
                data.buttons.push(b.innerText.trim().substring(0, 50));
            }
        });

        // Forms
        document.querySelectorAll('form').forEach(f => {
            data.forms.push({
                id: f.id,
                action: f.action
            });
        });

        return data;
    }"""
    )


def explore_qbo(context, categories=None):
    """Explora rotas do QBO."""
    page = get_qbo_page(context)
    results = {}

    if categories is None:
        categories = ["core", "wfs"]

    for category in categories:
        routes = QBO_ROUTES.get(category, [])
        results[category] = {}

        for route in routes:
            print(f"Explorando QBO: {route}...")
            result = navigate_qbo(page, route)

            if result["status"] == "OK":
                result["data"] = extract_page_data(page)

            results[category][route] = result

    return results


def explore_mineral(context):
    """Explora rotas do Mineral."""
    page = get_mineral_page(context)

    if not page:
        print("Mineral nao esta aberto. Abrindo via QBO...")
        qbo_page = get_qbo_page(context)
        page = open_mineral_from_qbo(qbo_page, context)

    if not page:
        return {"error": "Nao foi possivel abrir Mineral"}

    results = {}

    for route in MINERAL_ROUTES:
        print(f"Explorando Mineral: {route}...")
        result = navigate_mineral(page, route)

        if result["status"] == "OK":
            result["data"] = extract_page_data(page)

        results[route] = result

    return results


# ============================================================
# FUNCOES DE CAPTURA
# ============================================================


def capture_screenshots(context, output_dir, systems=None):
    """Captura screenshots de todos os sistemas."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    if systems is None:
        systems = ["qbo", "mineral"]

    results = {"timestamp": timestamp, "captures": []}

    if "qbo" in systems:
        qbo_dir = os.path.join(output_dir, f"qbo_{timestamp}")
        os.makedirs(qbo_dir, exist_ok=True)

        page = get_qbo_page(context)
        for category, routes in QBO_ROUTES.items():
            for route in routes:
                print(f"Capturando QBO: {route}...")
                navigate_qbo(page, route)
                filename = route.replace("/", "_")[1:] + ".png"
                filepath = os.path.join(qbo_dir, filename)
                page.screenshot(path=filepath)
                results["captures"].append(
                    {"system": "qbo", "route": route, "file": filepath}
                )

    if "mineral" in systems:
        mineral_dir = os.path.join(output_dir, f"mineral_{timestamp}")
        os.makedirs(mineral_dir, exist_ok=True)

        page = get_mineral_page(context)
        if not page:
            qbo_page = get_qbo_page(context)
            page = open_mineral_from_qbo(qbo_page, context)

        if page:
            for route in MINERAL_ROUTES:
                print(f"Capturando Mineral: {route}...")
                navigate_mineral(page, route)
                filename = route.replace("/", "_")[1:] + ".png"
                filepath = os.path.join(mineral_dir, filename)
                page.screenshot(path=filepath)
                results["captures"].append(
                    {"system": "mineral", "route": route, "file": filepath}
                )

    return results


# ============================================================
# HEALTH CHECK
# ============================================================


def health_check(context):
    """Executa health check dos sistemas."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "qbo": {},
        "mineral": {},
    }

    # QBO Checks
    page = get_qbo_page(context)

    checks = [
        ("/app/homepage", "Dashboard"),
        ("/app/employees", "Employees"),
        ("/app/payroll", "Payroll"),
        ("/app/timetracking", "Time"),
        ("/app/hr", "HR Advisor"),
    ]

    for route, name in checks:
        result = navigate_qbo(page, route)
        status = "PASS" if result["status"] == "OK" else "FAIL"
        results["qbo"][name] = {"route": route, "status": status}
        print(f"QBO {name}: {status}")

    # Mineral Check
    mineral_page = get_mineral_page(context)
    if not mineral_page:
        mineral_page = open_mineral_from_qbo(page, context)

    if mineral_page:
        result = navigate_mineral(mineral_page, "/dashboard")
        status = "PASS" if result["status"] == "OK" else "FAIL"
        results["mineral"]["Dashboard"] = {"status": status}
        print(f"Mineral Dashboard: {status}")
    else:
        results["mineral"]["Dashboard"] = {"status": "FAIL", "error": "Could not open"}
        print("Mineral Dashboard: FAIL")

    # Summary
    qbo_pass = sum(1 for v in results["qbo"].values() if v["status"] == "PASS")
    qbo_total = len(results["qbo"])
    mineral_pass = sum(1 for v in results["mineral"].values() if v["status"] == "PASS")
    mineral_total = len(results["mineral"])

    results["summary"] = {
        "qbo": f"{qbo_pass}/{qbo_total}",
        "mineral": f"{mineral_pass}/{mineral_total}",
        "overall": "PASS"
        if qbo_pass == qbo_total and mineral_pass == mineral_total
        else "FAIL",
    }

    print(
        f"\nSummary: QBO {results['summary']['qbo']}, Mineral {results['summary']['mineral']}"
    )
    print(f"Overall: {results['summary']['overall']}")

    return results


# ============================================================
# MAIN
# ============================================================


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "health_check"

    print("=" * 60)
    print(f"WFS EXPLORER - {command}")
    print("=" * 60)

    pw, browser, context, page = connect_browser()

    try:
        if command == "explore_qbo":
            results = explore_qbo(context)
            output_file = f"{OUTPUT_DIR}/qbo_exploration.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nSalvo: {output_file}")

        elif command == "explore_mineral":
            results = explore_mineral(context)
            output_file = f"{OUTPUT_DIR}/mineral_exploration.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nSalvo: {output_file}")

        elif command == "health_check":
            results = health_check(context)
            output_file = f"{OUTPUT_DIR}/health_check.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nSalvo: {output_file}")

        elif command == "capture_all":
            results = capture_screenshots(context, f"{OUTPUT_DIR}/screenshots")
            output_file = f"{OUTPUT_DIR}/capture_results.json"
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nSalvo: {output_file}")

        else:
            print(f"Comando desconhecido: {command}")
            print("Comandos: explore_qbo, explore_mineral, health_check, capture_all")

    finally:
        pw.stop()


if __name__ == "__main__":
    main()
