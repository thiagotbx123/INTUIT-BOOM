# -*- coding: utf-8 -*-
"""
Recaptura Automatica com Login Integrado
- Login automatico via layer1_login
- 10 segundos de espera
- NUNCA rejeita, apenas marca com flags
- Evidence notes tecnicas detalhadas
"""

import json
import os
import sys
import time
from datetime import datetime

from layer1_login import login, is_logged_in_qbo  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

WAIT_TIME = 10
OUTPUT_DIR_TCO = "EvidencePack/WinterRelease/TCO"
OUTPUT_DIR_CONSTR = "EvidencePack/WinterRelease/Construction"

# Features TCO que precisam recaptura
FEATURES_TCO = [
    {
        "ref": "WR-014",
        "name": "Benchmarking",
        "nav_steps": [
            ("goto", "https://qbo.intuit.com/app/reports"),
            ("wait", 5),
            ("click", "text=Performance center"),
            ("wait", 10),
        ],
        "fallback_url": "https://qbo.intuit.com/app/business-intelligence/kpi-scorecard",
    },
    {
        "ref": "WR-021",
        "name": "Seamless Desktop Migration",
        "nav_steps": [
            ("goto", "https://qbo.intuit.com/app/settings"),
            ("wait", 5),
            ("click", "text=Import data"),
            ("wait", 10),
        ],
        "fallback_url": "https://qbo.intuit.com/app/importdata",
    },
    {
        "ref": "WR-022",
        "name": "DFY Migration Experience",
        "nav_steps": [
            ("goto", "https://qbo.intuit.com/app/settings"),
            ("wait", 5),
            ("click", "text=Import data"),
            ("wait", 10),
        ],
        "fallback_url": "https://qbo.intuit.com/app/importdata",
    },
    {
        "ref": "WR-023",
        "name": "Feature Compatibility",
        "nav_steps": [
            ("goto", "https://qbo.intuit.com/app/settings"),
            ("wait", 5),
        ],
        "fallback_url": "https://qbo.intuit.com/app/settings",
    },
]

# Features Construction que precisam recaptura
FEATURES_CONSTRUCTION = [
    {
        "ref": "WR-018",
        "name": "Dimensions on Workflow",
        "nav_steps": [
            ("goto", "https://qbo.intuit.com/app/homepage"),
            ("wait", 3),
            (
                "click",
                '[data-testid="settings-gear"], [data-automation-id="settings-gear"]',
            ),
            ("wait", 2),
            ("click", "text=Workflows"),
            ("wait", 10),
        ],
        "fallback_url": "https://qbo.intuit.com/app/workflowautomation",
    },
    {
        "ref": "WR-020",
        "name": "Parallel Approval",
        "nav_steps": [
            ("goto", "https://qbo.intuit.com/app/homepage"),
            ("wait", 3),
            (
                "click",
                '[data-testid="settings-gear"], [data-automation-id="settings-gear"]',
            ),
            ("wait", 2),
            ("click", "text=Workflows"),
            ("wait", 10),
        ],
        "fallback_url": "https://qbo.intuit.com/app/workflowautomation",
    },
]


def capture_with_analysis(page, ref, name, output_dir, env):
    """Captura e analisa screenshot"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{ref}_{env}_{timestamp}_REFINED.png"
    filepath = os.path.join(output_dir, filename)

    # Capturar
    page.screenshot(path=filepath, full_page=False)
    size_kb = os.path.getsize(filepath) // 1024

    # Analisar
    title = page.title()
    url = page.url
    content = page.content().lower()

    has_loading = "loading" in content or "spinner" in content
    has_error = "sorry" in content or "404" in content or "sign-in" in url

    # Pegar headers visiveis
    try:
        headers = page.locator("h1, h2, h3").all_text_contents()
        visible_headers = [h.strip() for h in headers if h.strip()][:5]
    except Exception:
        visible_headers = []

    # Pegar empresa
    company = ""
    try:
        company_elem = page.locator(
            '[class*="company"], .company-name, [data-testid="company-name"]'
        ).first
        if company_elem:
            company = company_elem.text_content().strip()
    except Exception:
        pass

    # Gerar evidence notes tecnicas
    notes = []
    notes.append(f"FEATURE: {ref} - {name}")
    notes.append(f"ENVIRONMENT: {env}")
    notes.append(f"CAPTURE_TIME: {timestamp}")
    notes.append(f"URL: {url}")
    notes.append(f"PAGE_TITLE: {title}")
    if company:
        notes.append(f"COMPANY: {company}")
    notes.append(f"FILE_SIZE: {size_kb}KB")

    # Flags
    flags = []
    if "sign-in" in url:
        flags.append("LOGIN_PAGE")
    if has_loading:
        flags.append("LOADING_DETECTED")
    if has_error:
        flags.append("ERROR_CONTENT")
    if size_kb < 50:
        flags.append("VERY_SMALL_FILE")
    elif size_kb < 100:
        flags.append("SMALL_FILE")

    notes.append(f"FLAGS: {', '.join(flags) if flags else 'NONE'}")

    if visible_headers:
        notes.append(f"VISIBLE_HEADERS: {', '.join(visible_headers[:3])}")

    # Validacao tecnica
    if "sign-in" in url:
        notes.append("VALIDATION: LOGIN_PAGE - Session expired, requires re-login")
    elif has_error:
        notes.append("VALIDATION: ERROR_PAGE - Requires investigation")
    elif has_loading:
        notes.append("VALIDATION: LOADING_STATE - Content may be incomplete")
    elif size_kb < 100:
        notes.append("VALIDATION: REVIEW_REQUIRED - Small file size")
    else:
        notes.append("VALIDATION: CAPTURED_OK - Visual verification recommended")

    return {
        "filepath": filepath,
        "filename": filename,
        "size_kb": size_kb,
        "url": url,
        "title": title,
        "company": company,
        "has_loading": has_loading,
        "has_error": has_error,
        "visible_headers": visible_headers,
        "evidence_notes": "\n".join(notes),
        "flags": flags,
    }


def recapture_env(page, features, output_dir, env):
    """Recaptura todas as features de um ambiente"""
    results = []

    for feature in features:
        ref = feature["ref"]
        name = feature["name"]

        print(f"\n{'=' * 60}")
        print(f"Capturando {ref} - {name}")
        print(f"{'=' * 60}")

        # Tentar navegacao com steps
        for action, value in feature["nav_steps"]:
            try:
                if action == "goto":
                    print(f"  Navegando para: {value}")
                    page.goto(value, wait_until="domcontentloaded", timeout=30000)
                elif action == "wait":
                    print(f"  Aguardando {value} segundos...")
                    time.sleep(value)
                elif action == "click":
                    print(f"  Clicando em: {value}")
                    page.click(value, timeout=5000)
            except Exception as e:
                print(f"  Aviso: {str(e)[:50]}")

        # Aguardar tempo final
        print(f"  Aguardando {WAIT_TIME} segundos para carregamento completo...")
        time.sleep(WAIT_TIME)

        # Capturar
        result = capture_with_analysis(page, ref, name, output_dir, env)
        result["ref"] = ref
        result["name"] = name

        print(f"  Capturado: {result['filename']} ({result['size_kb']}KB)")
        print(f"  Flags: {result['flags']}")

        # Se muito pequeno ou erro, tentar fallback
        if (
            result["size_kb"] < 50
            or result["has_error"]
            or "LOGIN_PAGE" in result["flags"]
        ):
            print("  Tentando fallback URL...")
            try:
                page.goto(feature["fallback_url"], wait_until="domcontentloaded")
                time.sleep(WAIT_TIME)
                result = capture_with_analysis(page, ref, name, output_dir, env)
                result["ref"] = ref
                result["name"] = name
                result["used_fallback"] = True
                print(
                    f"  Fallback capturado: {result['filename']} ({result['size_kb']}KB)"
                )
            except Exception as e:
                print(f"  Fallback falhou: {str(e)[:50]}")

        results.append(result)

    return results


def main():
    print("=" * 70)
    print("RECAPTURA AUTOMATICA COM LOGIN INTEGRADO")
    print(f"Espera: {WAIT_TIME} segundos")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR_TCO, exist_ok=True)
    os.makedirs(OUTPUT_DIR_CONSTR, exist_ok=True)

    all_results = []

    # Menu
    print("\nQual ambiente recapturar?")
    print("1. TCO (WR-014, WR-021, WR-022, WR-023)")
    print("2. Construction (WR-018, WR-020)")
    print("3. Ambos")
    choice = input("Escolha (1/2/3): ").strip()

    # ===== TCO =====
    if choice in ["1", "3"]:
        print("\n" + "=" * 70)
        print("LOGIN TCO - Apex Tire")
        print("=" * 70)

        pw, browser, page = login("TCO", "apex")

        # Verificar se logou
        if not is_logged_in_qbo(page):
            print("[ERRO] Nao foi possivel logar no TCO")
        else:
            print("[OK] Logado no TCO")
            time.sleep(3)  # Estabilizar

            tco_results = recapture_env(page, FEATURES_TCO, OUTPUT_DIR_TCO, "TCO")
            all_results.extend(tco_results)

        pw.stop()

    # ===== CONSTRUCTION =====
    if choice in ["2", "3"]:
        print("\n" + "=" * 70)
        print("LOGIN CONSTRUCTION - Keystone")
        print("=" * 70)

        pw, browser, page = login("CONSTRUCTION", "construction")

        # Verificar se logou
        if not is_logged_in_qbo(page):
            print("[ERRO] Nao foi possivel logar no Construction")
        else:
            print("[OK] Logado no Construction")
            time.sleep(3)  # Estabilizar

            constr_results = recapture_env(
                page, FEATURES_CONSTRUCTION, OUTPUT_DIR_CONSTR, "CONSTRUCTION"
            )
            all_results.extend(constr_results)

        pw.stop()

    # Salvar resultados
    results_file = (
        f"docs/RECAPTURE_RESULTS_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    )
    os.makedirs("docs", exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO RECAPTURA")
    print("=" * 70)

    for r in all_results:
        status = "OK" if not r["flags"] else ", ".join(r["flags"])
        env = r.get("env", "N/A")
        print(f"[{env}] {r['ref']}: {r['size_kb']}KB - {status}")

    print(f"\nResultados: {results_file}")

    # Evidence notes
    print("\n" + "=" * 70)
    print("EVIDENCE NOTES")
    print("=" * 70)

    for r in all_results:
        print(f"\n--- {r['ref']} ({r.get('env', 'N/A')}) ---")
        print(r["evidence_notes"])


if __name__ == "__main__":
    main()
