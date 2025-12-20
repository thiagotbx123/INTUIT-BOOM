# -*- coding: utf-8 -*-
"""
WFS MAPPER - Login com SMS
==========================
Script para login no QBO com conta thiago@testbox.com (verificacao SMS)

Uso:
    python wfs_mapper_login.py

Aguarda codigo SMS do usuario para completar login.
"""

import time
import socket
import subprocess
import os
from playwright.sync_api import sync_playwright

# ============================================================
# CONFIGURACAO
# ============================================================

CDP_PORT = 9222
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.path.join(
    os.environ.get("TEMP", "C:\\Temp"), "tsa_qbo_chrome_profile"
)

# Credenciais
EMAIL = "thiago@testbox.com"
# Senha sera pedida se necessario

# ============================================================
# FUNCOES AUXILIARES
# ============================================================


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


def connect_chrome():
    """Conecta ao Chrome via CDP."""
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

        print("[OK] Conectado ao Chrome")
        return pw, browser, page

    except Exception as e:
        pw.stop()
        raise ConnectionError(f"Erro ao conectar: {e}")


def wait_for_sms_code():
    """Aguarda usuario digitar codigo SMS."""
    print("\n" + "=" * 50)
    print("AGUARDANDO CODIGO SMS")
    print("=" * 50)
    code = input("Digite o codigo SMS recebido: ").strip()
    return code


def login_with_sms(page, email, password=None):
    """
    Login com verificacao SMS.

    Args:
        page: Playwright page
        email: Email para login
        password: Senha (opcional, sera pedida se necessario)
    """
    print("\n" + "=" * 50)
    print(f"LOGIN: {email}")
    print("=" * 50)

    # Navegar para pagina de login
    print("[1/5] Navegando para login...")
    page.goto("https://accounts.intuit.com/app/sign-in")
    time.sleep(3)

    # Verificar se ja esta logado
    if "qbo.intuit.com" in page.url:
        print("[OK] Ja esta logado no QBO!")
        return True

    # Procurar conta salva ou preencher email
    print(f"[2/5] Procurando conta {email}...")
    try:
        # Tentar encontrar conta salva
        saved = page.locator(f"text={email}").first
        if saved.is_visible(timeout=3000):
            print("      Conta encontrada, clicando...")
            saved.click()
            time.sleep(3)
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
        except Exception as e:
            print(f"      [WARN] Erro ao preencher email: {e}")

    # Verificar se pede senha
    print("[3/5] Verificando senha...")
    try:
        password_input = page.get_by_test_id("currentPasswordInput")
        if password_input.is_visible(timeout=3000):
            if not password:
                password = input("Digite a senha: ").strip()
            print("      Preenchendo senha...")
            password_input.fill(password)
            time.sleep(0.5)
            page.get_by_test_id("passwordVerificationContinueButton").click()
            time.sleep(5)
    except Exception:
        print("      Senha nao solicitada")

    # Verificar se pede SMS
    print("[4/5] Verificando SMS...")
    try:
        # Procurar opcao de SMS
        sms_option = page.locator("text=SMS").first
        if sms_option.is_visible(timeout=3000):
            print("      Selecionando opcao SMS...")
            sms_option.click()
            time.sleep(3)
    except Exception:
        pass

    # Verificar se tem input de codigo
    try:
        # Diferentes test-ids possiveis para SMS
        sms_inputs = [
            page.get_by_test_id("VerifyOtpInput"),
            page.get_by_test_id("OtpInput"),
            page.locator('input[type="tel"]'),
            page.locator('input[placeholder*="code"]'),
        ]

        for sms_input in sms_inputs:
            try:
                if sms_input.is_visible(timeout=2000):
                    # Aguardar codigo SMS
                    code = wait_for_sms_code()
                    print(f"      Preenchendo codigo: {code}")
                    sms_input.fill(code)
                    time.sleep(0.5)

                    # Tentar clicar em submit
                    try:
                        page.get_by_test_id("VerifyOtpSubmitButton").click()
                    except Exception:
                        try:
                            page.locator('button[type="submit"]').click()
                        except Exception:
                            page.keyboard.press("Enter")

                    time.sleep(5)
                    break
            except Exception:
                continue
    except Exception as e:
        print(f"      [WARN] Erro ao processar SMS: {e}")

    # Skip passkey prompt
    print("[5/5] Finalizando...")
    try:
        skip = page.locator(
            'button:has-text("Skip"), button:has-text("Ignorar"), button:has-text("Agora")'
        )
        if skip.is_visible(timeout=2000):
            skip.click()
            time.sleep(2)
    except Exception:
        pass

    # Verificar resultado
    time.sleep(3)
    if "qbo.intuit.com" in page.url:
        print("\n[OK] LOGIN COMPLETO!")
        return True
    else:
        print(f"\n[INFO] URL atual: {page.url}")
        return False


def navigate_to_url(page, url):
    """Navega para URL especifica."""
    print(f"\n[INFO] Navegando para: {url[:60]}...")
    page.goto(url)
    time.sleep(5)
    print(f"[OK] URL atual: {page.url[:60]}...")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("WFS MAPPER - Login com SMS")
    print("=" * 60)

    # URL fornecida pelo usuario
    target_url = "https://qbo.intuit.com/app/homepage?locale=en-us&intuit_tid=1-6945601e-42b7c25606e9ae5a1ffebcc0"

    # Conectar ao Chrome
    pw, browser, page = connect_chrome()

    try:
        # Navegar para URL
        navigate_to_url(page, target_url)

        # Se nao estiver logado, fazer login
        if "sign-in" in page.url or "accounts.intuit.com" in page.url:
            login_with_sms(page, EMAIL)
        elif "qbo.intuit.com" in page.url:
            print("[OK] Ja esta no QBO!")

        # Aguardar usuario
        print("\n" + "=" * 60)
        print("BROWSER PRONTO PARA MAPEAMENTO")
        print("=" * 60)
        print("O Chrome esta aberto e conectado.")
        print("Voce pode navegar manualmente ou executar comandos.")
        print("\nPressione ENTER para encerrar...")
        input()

    finally:
        print("\n[INFO] Encerrando...")
        pw.stop()
