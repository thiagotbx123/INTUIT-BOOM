# -*- coding: utf-8 -*-
"""
FEATURE VALIDATOR - Metodo Padronizado v2.0
Winter Release FY26 - Refinado 2025-12-29

Processo estruturado para validacao de features QBO:
1. Login automatico
2. Navegacao com fallbacks
3. Captura com espera adequada
4. Validacao com flags (nunca rejeita)
5. Evidence notes tecnicas
6. Tratamento de NOT_AVAILABLE
"""

from playwright.sync_api import sync_playwright
import time
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar modulo de login
try:
    from layer1_login import login  # noqa: F401
except ImportError:
    print("AVISO: layer1_login.py nao encontrado")


# =============================================================================
# CONFIGURACOES PADRAO
# =============================================================================

CONFIG = {
    "WAIT_TIME_MIN": 30,  # Tempo minimo de espera (segundos)
    "WAIT_TIME_MAX": 60,  # Tempo maximo antes de desistir
    "SCREENSHOT_TIMEOUT": 60000,  # Timeout para screenshot (ms)
    "NAVIGATION_TIMEOUT": 60000,  # Timeout para navegacao (ms)
    # Thresholds de qualidade (KB)
    "SIZE_EXCELLENT": 250,
    "SIZE_GOOD": 150,
    "SIZE_ACCEPTABLE": 100,
    "SIZE_WEAK": 50,
    "SIZE_ERROR_PAGE": 139,  # Tamanho tipico de pagina 404
    # Output directories
    "OUTPUT_TCO": "EvidencePack/WinterRelease/TCO",
    "OUTPUT_CONSTRUCTION": "EvidencePack/WinterRelease/Construction",
}


# =============================================================================
# FLAGS DE VALIDACAO
# =============================================================================


class ValidationFlags:
    """Flags para marcar problemas detectados (nunca rejeita, apenas marca)"""

    LOGIN_PAGE = "LOGIN_PAGE"  # Capturou pagina de login
    LOADING_DETECTED = "LOADING_DETECTED"  # Spinner visivel
    ERROR_CONTENT = "ERROR_CONTENT"  # Conteudo de erro (sorry, 404)
    VERY_SMALL_FILE = "VERY_SMALL_FILE"  # < 50KB
    SMALL_FILE = "SMALL_FILE"  # 50-100KB
    ERROR_PAGE_404 = "ERROR_PAGE_404"  # Pagina 404 confirmada
    NOT_AVAILABLE = "NOT_AVAILABLE"  # Feature nao disponivel no ambiente


# =============================================================================
# STATUS DE FEATURE
# =============================================================================


class FeatureStatus:
    """Status possiveis para uma feature"""

    PASS = "PASS"  # Feature funciona conforme esperado
    PARTIAL = "PARTIAL"  # Feature existe mas com limitacoes
    NOT_AVAILABLE = "NOT_AVAILABLE"  # Feature nao habilitada/acessivel
    FAIL = "FAIL"  # Feature deveria funcionar mas tem bug
    NA = "N/A"  # Feature nao aplicavel (ex: documentacao)
    REVIEW = "REVIEW"  # Requer revisao manual


# =============================================================================
# ANALISE DE PAGINA
# =============================================================================


def analyze_page(page) -> Dict:
    """Analisa conteudo da pagina para detectar problemas"""

    analysis = {
        "url": page.url,
        "title": "",
        "has_loading": False,
        "has_error": False,
        "is_login_page": False,
        "is_404": False,
        "visible_headers": [],
        "company": "",
        "flags": [],
    }

    try:
        analysis["title"] = page.title()
    except Exception:
        analysis["title"] = "Unknown"

    # Detectar pagina de login
    if "sign-in" in page.url.lower():
        analysis["is_login_page"] = True
        analysis["flags"].append(ValidationFlags.LOGIN_PAGE)

    # Verificar conteudo
    try:
        content = page.content().lower()

        # Detectar erro/404
        if "we're sorry" in content or "can't find" in content:
            analysis["is_404"] = True
            analysis["flags"].append(ValidationFlags.ERROR_PAGE_404)

        if "sorry" in content or "404" in content or "not found" in content:
            analysis["has_error"] = True
            analysis["flags"].append(ValidationFlags.ERROR_CONTENT)

        # Detectar loading
        if "loading" in content or "spinner" in content:
            analysis["has_loading"] = True
            analysis["flags"].append(ValidationFlags.LOADING_DETECTED)
    except Exception:
        pass

    # Detectar loading spinner via seletores
    spinner_selectors = [".loading", '[class*="spinner"]', '[class*="loading"]']
    for sel in spinner_selectors:
        try:
            if page.locator(sel).count() > 0:
                analysis["has_loading"] = True
                if ValidationFlags.LOADING_DETECTED not in analysis["flags"]:
                    analysis["flags"].append(ValidationFlags.LOADING_DETECTED)
                break
        except Exception:
            pass

    # Pegar headers visiveis
    try:
        headers = page.locator("h1, h2, h3").all_text_contents()
        analysis["visible_headers"] = [h.strip() for h in headers if h.strip()][:5]
    except Exception:
        pass

    # Pegar empresa
    try:
        company_selectors = [
            '[data-testid="company-name"]',
            '[data-testid="company-picker-button"]',
            ".company-name",
        ]
        for sel in company_selectors:
            try:
                elem = page.locator(sel).first
                if elem.is_visible(timeout=1000):
                    analysis["company"] = elem.text_content().strip()
                    break
            except Exception:
                pass
    except Exception:
        pass

    return analysis


# =============================================================================
# CAPTURA DE FEATURE
# =============================================================================


def capture_feature(
    page,
    ref: str,
    name: str,
    url: str,
    output_dir: str,
    env: str,
    fallback_url: Optional[str] = None,
    wait_time: int = None,
) -> Dict:
    """
    Captura uma feature com processo padronizado.

    NUNCA rejeita - apenas marca com flags.

    Args:
        page: Playwright page object
        ref: Referencia da feature (ex: WR-014)
        name: Nome da feature
        url: URL primaria
        output_dir: Diretorio de saida
        env: Ambiente (TCO, CONSTRUCTION)
        fallback_url: URL alternativa se primaria falhar
        wait_time: Tempo de espera (usa CONFIG se None)

    Returns:
        Dict com resultado da captura
    """

    wait_time = wait_time or CONFIG["WAIT_TIME_MIN"]

    result = {
        "ref": ref,
        "name": name,
        "env": env,
        "timestamp": datetime.now().isoformat(),
        "url_attempted": url,
        "url_captured": "",
        "screenshot_path": "",
        "size_kb": 0,
        "quality": "",
        "status": FeatureStatus.REVIEW,
        "flags": [],
        "evidence_notes": "",
        "analysis": {},
    }

    print(f"\n{'=' * 60}")
    print(f"Capturando {ref} - {name}")
    print(f"{'=' * 60}")

    # 1. NAVEGACAO
    print(f"  Navegando para: {url}")
    try:
        page.goto(
            url, wait_until="domcontentloaded", timeout=CONFIG["NAVIGATION_TIMEOUT"]
        )
    except Exception as e:
        print(f"  ERRO navegacao: {str(e)[:50]}")
        result["flags"].append("NAVIGATION_ERROR")

    # 2. ESPERA
    print(f"  Aguardando {wait_time}s...")
    time.sleep(wait_time)

    # 3. ANALISE
    analysis = analyze_page(page)
    result["analysis"] = analysis
    result["url_captured"] = analysis["url"]
    result["flags"].extend(analysis["flags"])

    # 4. CAPTURA
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{ref}_{env}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    try:
        page.screenshot(path=filepath, timeout=CONFIG["SCREENSHOT_TIMEOUT"])
        size_kb = os.path.getsize(filepath) // 1024
        result["screenshot_path"] = filepath
        result["size_kb"] = size_kb
        print(f"  Capturado: {filename} ({size_kb}KB)")
    except Exception as e:
        print(f"  ERRO screenshot: {str(e)[:50]}")
        result["flags"].append("SCREENSHOT_ERROR")
        size_kb = 0

    # 5. FLAGS DE TAMANHO
    if size_kb < CONFIG["SIZE_WEAK"]:
        result["flags"].append(ValidationFlags.VERY_SMALL_FILE)
    elif size_kb < CONFIG["SIZE_ACCEPTABLE"]:
        result["flags"].append(ValidationFlags.SMALL_FILE)

    # 6. QUALIDADE
    if size_kb >= CONFIG["SIZE_EXCELLENT"]:
        result["quality"] = "EXCELLENT"
    elif size_kb >= CONFIG["SIZE_GOOD"]:
        result["quality"] = "GOOD"
    elif size_kb >= CONFIG["SIZE_ACCEPTABLE"]:
        result["quality"] = "ACCEPTABLE"
    elif size_kb >= CONFIG["SIZE_WEAK"]:
        result["quality"] = "WEAK"
    else:
        result["quality"] = "INVALID"

    # 7. FALLBACK SE NECESSARIO
    if (
        analysis["is_404"] or analysis["is_login_page"] or size_kb < CONFIG["SIZE_WEAK"]
    ) and fallback_url:
        print(f"  Tentando fallback: {fallback_url}")
        try:
            page.goto(
                fallback_url,
                wait_until="domcontentloaded",
                timeout=CONFIG["NAVIGATION_TIMEOUT"],
            )
            time.sleep(wait_time)

            # Recapturar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"{ref}_{env}_{timestamp}_fallback.png"
            filepath = os.path.join(output_dir, filename)

            page.screenshot(path=filepath, timeout=CONFIG["SCREENSHOT_TIMEOUT"])
            size_kb = os.path.getsize(filepath) // 1024

            result["screenshot_path"] = filepath
            result["size_kb"] = size_kb
            result["url_captured"] = page.url
            result["flags"].append("USED_FALLBACK")

            print(f"  Fallback capturado: {filename} ({size_kb}KB)")
        except Exception as e:
            print(f"  Fallback falhou: {str(e)[:50]}")

    # 8. DETERMINAR STATUS
    if analysis["is_404"]:
        result["status"] = FeatureStatus.NOT_AVAILABLE
    elif analysis["is_login_page"]:
        result["status"] = FeatureStatus.FAIL
        result["flags"].append("SESSION_EXPIRED")
    elif analysis["has_loading"] and size_kb < CONFIG["SIZE_ACCEPTABLE"]:
        result["status"] = FeatureStatus.REVIEW
    elif size_kb >= CONFIG["SIZE_ACCEPTABLE"] and not analysis["has_error"]:
        result["status"] = FeatureStatus.PASS
    else:
        result["status"] = FeatureStatus.REVIEW

    # 9. EVIDENCE NOTES
    result["evidence_notes"] = generate_evidence_notes(result, analysis)

    print(f"  Status: {result['status']}")
    print(f"  Flags: {result['flags']}")

    return result


# =============================================================================
# EVIDENCE NOTES
# =============================================================================


def generate_evidence_notes(result: Dict, analysis: Dict) -> str:
    """Gera evidence notes tecnicas detalhadas"""

    notes = []

    # Header
    notes.append(f"FEATURE: {result['ref']} - {result['name']}")
    notes.append(f"ENVIRONMENT: {result['env']}")
    notes.append(f"CAPTURE_TIME: {result['timestamp']}")
    notes.append(f"URL: {result['url_captured']}")
    notes.append(f"PAGE_TITLE: {analysis.get('title', 'N/A')}")

    if analysis.get("company"):
        notes.append(f"COMPANY: {analysis['company']}")

    notes.append(f"FILE_SIZE: {result['size_kb']}KB")
    notes.append(f"QUALITY: {result['quality']}")

    # Flags
    flags_str = ", ".join(result["flags"]) if result["flags"] else "NONE"
    notes.append(f"FLAGS: {flags_str}")

    # Headers visiveis
    if analysis.get("visible_headers"):
        headers_str = ", ".join(analysis["visible_headers"][:3])
        notes.append(f"VISIBLE_HEADERS: {headers_str}")

    # Validacao
    if result["status"] == FeatureStatus.PASS:
        notes.append("VALIDATION: PASS - Feature captured successfully")
    elif result["status"] == FeatureStatus.NOT_AVAILABLE:
        notes.append(
            "VALIDATION: NOT_AVAILABLE - Feature not enabled in this environment"
        )
    elif result["status"] == FeatureStatus.REVIEW:
        notes.append("VALIDATION: REVIEW - Manual verification required")
    elif result["status"] == FeatureStatus.FAIL:
        notes.append("VALIDATION: FAIL - Capture failed (check flags)")
    else:
        notes.append(f"VALIDATION: {result['status']}")

    return "\n".join(notes)


# =============================================================================
# BATCH CAPTURE
# =============================================================================


def capture_features_batch(
    features: List[Dict], env: str, output_dir: str, page=None, auto_login: bool = True
) -> List[Dict]:
    """
    Captura multiplas features em batch.

    Args:
        features: Lista de dicts com {ref, name, url, fallback_url?}
        env: Ambiente (TCO, CONSTRUCTION)
        output_dir: Diretorio de saida
        page: Playwright page (opcional, cria novo se None)
        auto_login: Se deve fazer login automatico

    Returns:
        Lista de resultados
    """

    results = []
    pw = None

    try:
        if page is None:
            if auto_login:
                pw, browser, page = login(env, env.lower())
            else:
                pw = sync_playwright().start()
                browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
                context = browser.contexts[0]
                page = context.pages[0]

        for feature in features:
            result = capture_feature(
                page=page,
                ref=feature["ref"],
                name=feature["name"],
                url=feature["url"],
                output_dir=output_dir,
                env=env,
                fallback_url=feature.get("fallback_url"),
                wait_time=feature.get("wait_time", CONFIG["WAIT_TIME_MIN"]),
            )
            results.append(result)

    finally:
        if pw:
            pw.stop()

    return results


# =============================================================================
# EXPORTACAO
# =============================================================================


def export_results_json(results: List[Dict], filepath: str):
    """Exporta resultados para JSON"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)


def export_summary(results: List[Dict]) -> str:
    """Gera resumo textual dos resultados"""

    lines = []
    lines.append("=" * 60)
    lines.append("RESUMO DE VALIDACAO")
    lines.append("=" * 60)

    for r in results:
        status_icon = {
            FeatureStatus.PASS: "[OK]",
            FeatureStatus.PARTIAL: "[PARTIAL]",
            FeatureStatus.NOT_AVAILABLE: "[N/A]",
            FeatureStatus.FAIL: "[FAIL]",
            FeatureStatus.REVIEW: "[REVIEW]",
            FeatureStatus.NA: "[N/A]",
        }.get(r["status"], "[??]")

        flags = ", ".join(r["flags"][:2]) if r["flags"] else "none"
        lines.append(
            f"{status_icon} {r['ref']} ({r['env']}): {r['size_kb']}KB - {flags}"
        )

    # Estatisticas
    total = len(results)
    passed = sum(1 for r in results if r["status"] == FeatureStatus.PASS)
    failed = sum(
        1 for r in results if r["status"] in [FeatureStatus.FAIL, FeatureStatus.REVIEW]
    )
    na = sum(1 for r in results if r["status"] == FeatureStatus.NOT_AVAILABLE)

    lines.append("")
    lines.append(f"Total: {total} | Pass: {passed} | Review: {failed} | N/A: {na}")

    return "\n".join(lines)


# =============================================================================
# MAIN (para testes)
# =============================================================================

if __name__ == "__main__":
    print("Feature Validator v2.0")
    print(
        "Use: from qbo_checker.feature_validator import capture_feature, capture_features_batch"
    )
