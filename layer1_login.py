# -*- coding: utf-8 -*-
"""
CAMADA 1 - LOGIN/CONEXAO QBO
============================
Versao solida e testada em 2025-12-06.

Uso:
    from layer1_login import connect_qbo, login_tco, start_round

    # Se Chrome ja esta logado no QBO:
    pw, browser, page = connect_qbo()

    # Login completo TCO (abre Chrome, loga, seleciona empresa):
    pw, browser, page = login_tco('apex')
    pw, browser, page = login_tco('consolidated')

    # Alias para login_tco:
    pw, browser, page = start_round('TCO', 'apex')
"""

import time
import socket
import subprocess
import os
import hmac
import hashlib
import struct
import base64
from playwright.sync_api import sync_playwright

# ============================================================
# CONFIGURACAO
# ============================================================

CDP_PORT = 9222
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.path.join(
    os.environ.get("TEMP", "C:\\Temp"), "tsa_qbo_chrome_profile"
)

# ============================================================
# CREDENCIAIS POR PROJETO
# ============================================================

PROJECTS = {
    "TCO": {
        "name": "TCO",
        "email": "quickbooks-testuser-tco-tbxdemo@tbxofficial.com",
        "password": "TestBox!23",
        "totp_secret": "RP4MFT45ZY5EYGMRIPEANJA6YFKHV5O7",
        "company_ids": {
            "consolidated": "9341455649090852",
            "global": "9341455130196737",
            "apex": "9341455130166501",
        },
        "companies": {
            "consolidated": "Vista consolidada",
            "global": "Global Tread Distributors, LLC",
            "apex": "Apex Tire & Auto Retail, LLC",
            "traction": "Traction Control Outfitters, LLC",
            "roadready": "RoadReady Service Solutions, LLC",
        },
        "default_company": "apex",
    },
    "CONSTRUCTION": {
        "name": "CONSTRUCTION SALES",
        "email": "quickbooks-test-account@tbxofficial.com",
        "password": "TestBox123!",
        "totp_secret": "23CIWY3QYCOXJRKZYG6YKR7HUYVPLPEL",
        "company_ids": {},  # TODO: Capturar IDs das companies
        "companies": {
            "consolidated": "Vista consolidada",
            "construction": "Keystone Construction (Par.)",
            "bluecraft": "Keystone BlueCraft",
            "canopy": "KeyStone Canopy",
            "ecocraft": "KeyStone Ecocraft",
            "ironcraft": "KeyStone Ironcraft",
            "stonecraft": "KeyStone Stonecraft",
        },
        "default_company": "construction",
    },
    "PRODUCT": {
        "name": "PRODUCT TEAM",
        "email": "quickbooks-tbx-product-team-test@tbxofficial.com",
        "password": "TestBox123!",
        "totp_secret": "23CIWY3QYCOXJRKZYG6YKR7HUYVPLPEL",
        "company_ids": {},  # TODO: Capturar IDs das companies
        "companies": {},
        "default_company": None,
    },
    "TCO_DEMO": {
        "name": "TCO DEMO",
        "email": "quickbooks-tco-tbxdemo@tbxofficial.com",
        "password": "TestBox123!",
        "totp_secret": "23CIWY3QYCOXJRKZYG6YKR7HUYVPLPEL",
        "company_ids": {},  # TODO: Capturar IDs das companies
        "companies": {},
        "default_company": None,
    },
}

# Aliases para facilitar
PROJECT_ALIASES = {
    "tco": "TCO",
    "construction": "CONSTRUCTION",
    "product": "PRODUCT",
    "tco_demo": "TCO_DEMO",
    "1": "CONSTRUCTION",
    "2": "TCO",
    "3": "PRODUCT",
    "4": "TCO_DEMO",
}

# ============================================================
# FUNCOES AUXILIARES
# ============================================================


def generate_totp(secret):
    """Gera codigo TOTP de 6 digitos."""
    padding = "=" * ((8 - len(secret) % 8) % 8)
    key = base64.b32decode(secret.upper() + padding)
    counter = int(time.time() // 30)
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    truncated = struct.unpack(">I", hmac_hash[offset : offset + 4])[0]
    code = (truncated & 0x7FFFFFFF) % 1000000
    return str(code).zfill(6)


def is_port_open(port=CDP_PORT):
    """Verifica se a porta CDP esta aberta."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_chrome():
    """Inicia Chrome com CDP se nao estiver rodando."""
    if is_port_open():
        print("[OK] Chrome ja rodando na porta 9222")
        return True

    print("[INFO] Iniciando Chrome...")
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
    ]

    DETACHED_PROCESS = 0x00000008
    CREATE_BREAKAWAY_FROM_JOB = 0x01000000

    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB,
        start_new_session=True,
        close_fds=True,
    )

    for _ in range(30):
        if is_port_open():
            time.sleep(1)
            print("[OK] Chrome iniciado")
            return True
        time.sleep(0.5)

    print("[ERRO] Nao foi possivel iniciar Chrome")
    return False


def get_project(project_name):
    """Retorna config do projeto, resolvendo aliases."""
    key = PROJECT_ALIASES.get(project_name.lower(), project_name.upper())
    project = PROJECTS.get(key)
    if not project:
        available = list(PROJECTS.keys())
        raise ValueError(
            f"Projeto '{project_name}' nao encontrado. Disponiveis: {available}"
        )
    return project


def get_switch_url(project, company_key):
    """Retorna URL para trocar de company."""
    company_ids = project.get("company_ids", {})
    company_id = company_ids.get(company_key)
    if company_id:
        return f"https://qbo.intuit.com/app/multiEntitySwitchCompany?companyId={company_id}"
    return None


# ============================================================
# FUNCOES PRINCIPAIS - CAMADA 1
# ============================================================


def connect_qbo():
    """
    Conecta ao Chrome via CDP e retorna (playwright, browser, page).
    Assume que o Chrome ja esta aberto.

    Returns:
        tuple: (playwright, browser, page)
    """
    if not is_port_open():
        if not start_chrome():
            raise ConnectionError("Chrome nao esta rodando na porta 9222")

    pw = sync_playwright().start()

    try:
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")

        if browser.contexts and browser.contexts[0].pages:
            context = browser.contexts[0]
            page = context.pages[0]
        else:
            context = browser.new_context()
            page = context.new_page()

        print("[OK] Conectado")
        return pw, browser, page

    except Exception as e:
        pw.stop()
        raise ConnectionError(f"Erro ao conectar: {e}")


def login(project_name="TCO", company=None):
    """
    Login completo no QBO com qualquer projeto.

    Fluxo:
    1. Inicia Chrome se necessario
    2. Navega para login Intuit
    3. Seleciona conta salva ou preenche credenciais
    4. Preenche senha se necessario
    5. Preenche TOTP se necessario
    6. Seleciona company

    Args:
        project_name: 'TCO', 'CONSTRUCTION', 'PRODUCT', 'TCO_DEMO' (ou aliases)
        company: Nome da company ou None para default do projeto

    Returns:
        tuple: (playwright, browser, page)

    Exemplos:
        login('TCO', 'apex')
        login('TCO', 'consolidated')
        login('CONSTRUCTION', 'sales')
        login('construction')  # Usa default_company
    """
    # Resolver projeto
    project = get_project(project_name)

    # Resolver company
    if company is None:
        company = project.get("default_company")

    company_name = (
        project.get("companies", {}).get(company, company) if company else "default"
    )

    print("=" * 50)
    print(f"CAMADA 1 - LOGIN {project['name']}")
    print(f"Company: {company_name}")
    print("=" * 50)

    # Conectar ao Chrome
    pw, browser, page = connect_qbo()
    current_url = page.url

    # Se ja esta no QBO, so troca company se necessario
    if "qbo.intuit.com" in current_url:
        print("[OK] Ja esta no QBO")
        if company:
            switch_url = get_switch_url(project, company)
            if switch_url:
                print(f"[INFO] Trocando para {company}...")
                page.goto(switch_url)
                time.sleep(5)
        return pw, browser, page

    # Navegar para login
    print("[1/5] Navegando para login...")
    page.goto("https://accounts.intuit.com/app/sign-in")
    time.sleep(3)

    # Procurar conta salva
    print(f"[2/5] Procurando conta {project['name']}...")
    email = project["email"]
    email_prefix = email.split("@")[0]  # quickbooks-testuser-tco-tbxdemo

    try:
        # Tentar encontrar conta salva pelo prefixo do email
        saved = page.locator(f"text={email_prefix}").first
        if saved.is_visible(timeout=3000):
            print("      Conta encontrada, clicando...")
            saved.click()
            time.sleep(4)
        else:
            raise Exception("Conta nao visivel")
    except Exception:
        # Preencher email manualmente
        print("      Preenchendo email...")
        try:
            email_input = page.get_by_test_id("IdentifierFirstIdentifierInput")
            email_input.wait_for(state="visible", timeout=5000)
            email_input.fill(email)
            time.sleep(0.5)
            page.get_by_test_id("IdentifierFirstSubmitButton").click()
            time.sleep(3)
        except Exception:
            pass

    # Verificar tela de verificacao de identidade
    try:
        password_option = page.locator("text=Introduza a palavra-passe").first
        if password_option.is_visible(timeout=3000):
            print("[3/5] Selecionando opcao senha...")
            password_option.click()
            time.sleep(3)
    except Exception:
        pass

    # Preencher senha
    print("[3/5] Verificando senha...")
    try:
        password_input = page.get_by_test_id("currentPasswordInput")
        if password_input.is_visible(timeout=5000):
            print("      Preenchendo senha...")
            password_input.fill(project["password"])
            time.sleep(0.5)
            page.get_by_test_id("passwordVerificationContinueButton").click()
            time.sleep(5)
    except Exception:
        pass

    # Preencher TOTP
    print("[4/5] Verificando TOTP...")
    try:
        totp_input = page.get_by_test_id("VerifySoftTokenInput")
        if totp_input.is_visible(timeout=5000):
            remaining = 30 - (int(time.time()) % 30)
            if remaining < 5:
                print(f"      Aguardando TOTP fresco ({remaining}s)...")
                time.sleep(remaining + 1)
            code = generate_totp(project["totp_secret"])
            print(f"      TOTP: {code}")
            totp_input.fill(code)
            time.sleep(0.5)
            page.get_by_test_id("VerifySoftTokenSubmitButton").click()
            time.sleep(5)
    except Exception:
        pass

    # Skip passkey prompt
    try:
        skip = page.locator(
            'button:has-text("Skip"), button:has-text("Ignorar"), button:has-text("Agora")'
        )
        if skip.is_visible(timeout=2000):
            skip.click()
            time.sleep(2)
    except Exception:
        pass

    # Tratar pagina account-manager (algumas contas passam por aqui)
    time.sleep(2)
    if "account-manager" in page.url:
        print("[INFO] Pagina account-manager detectada, redirecionando para QBO...")
        page.goto("https://qbo.intuit.com/app/homepage")
        time.sleep(5)

    # Selecionar company
    if company:
        print(f"[5/5] Selecionando company: {company}...")
    else:
        print("[5/5] Aguardando selecao de company...")
    time.sleep(2)

    # Verificar se esta na tela de selecao de empresa
    page_content = page.content().lower()
    if "restaure" in page_content or "restore" in page_content:
        if company and company_name:
            try:
                company_btn = page.locator(f"text={company_name}").first
                if company_btn.is_visible(timeout=5000):
                    company_btn.click()
                    time.sleep(10)
            except Exception:
                # Fallback: tentar texto parcial
                try:
                    partial = company_name.split()[0]  # Primeira palavra
                    page.locator(f"text={partial}").first.click()
                    time.sleep(10)
                except Exception:
                    pass

    # Verificar resultado
    final_url = page.url
    if "qbo.intuit.com" in final_url:
        print("")
        print("=" * 50)
        print("LOGIN COMPLETO!")
        print(f"Projeto: {project['name']}")
        print(f"Company: {company_name}")
        print(f"URL: {final_url[:60]}...")
        print("=" * 50)
    else:
        print(f"[WARN] URL final: {final_url}")

    return pw, browser, page


def login_tco(company="apex"):
    """Alias para login('TCO', company). Compatibilidade."""
    return login("TCO", company)


def start_round(project="TCO", company=None):
    """
    Alias para login().
    Mantido para compatibilidade com scripts antigos.

    Args:
        project: 'TCO', 'CONSTRUCTION', 'PRODUCT', 'TCO_DEMO'
        company: Nome da company ou None para default

    Returns:
        tuple: (playwright, browser, page)
    """
    return login(project, company)


def go_home(page):
    """Navega para homepage do QBO."""
    page.goto("https://qbo.intuit.com/app/homepage")
    time.sleep(3)
    return page


def switch_company(page, project_name, company):
    """Troca de company via URL."""
    project = get_project(project_name)
    switch_url = get_switch_url(project, company)
    if switch_url:
        print(f"[INFO] Trocando para {company}...")
        page.goto(switch_url)
        time.sleep(5)
        return True
    return False


def list_projects():
    """Lista todos os projetos disponiveis."""
    print("\nPROJETOS DISPONIVEIS:")
    print("=" * 60)
    for key, proj in PROJECTS.items():
        companies = list(proj.get("companies", {}).keys())
        default = proj.get("default_company", "-")
        print(f"\n[{key}] {proj['name']}")
        print(f"    Email: {proj['email']}")
        print(f"    Companies: {', '.join(companies) if companies else 'N/A'}")
        print(f"    Default: {default}")


# ============================================================
# TESTE
# ============================================================

if __name__ == "__main__":
    import sys

    # Ajuda
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print("""
CAMADA 1 - LOGIN QBO
====================

Uso:
    python layer1_login.py                    # Login TCO/apex (default)
    python layer1_login.py TCO apex           # Login TCO/apex
    python layer1_login.py TCO consolidated   # Login TCO/consolidated
    python layer1_login.py CONSTRUCTION       # Login Construction/sales
    python layer1_login.py --list             # Lista projetos

Projetos: TCO, CONSTRUCTION, PRODUCT, TCO_DEMO
        """)
        sys.exit(0)

    # Listar projetos
    if len(sys.argv) > 1 and sys.argv[1] in ["--list", "-l", "list"]:
        list_projects()
        sys.exit(0)

    # Pegar argumentos
    project = sys.argv[1] if len(sys.argv) > 1 else "TCO"
    company = sys.argv[2] if len(sys.argv) > 2 else None

    print("=" * 50)
    print("TESTE CAMADA 1 - LOGIN QBO")
    print("=" * 50)

    pw, browser, page = login(project, company)
    print(f"\nURL final: {page.url}")
    print("\n[OK] CAMADA 1 funcionando!")

    pw.stop()
