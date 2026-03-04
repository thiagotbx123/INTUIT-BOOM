import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Users\adm_r\intuit-boom")

from qbo_checker.login import ensure_logged_in
from qbo_checker.screenshot import generate_filename, capture_screenshot
import time

print("Conectando ao Chrome...")
pw, browser, page = ensure_logged_in("TCO")
time.sleep(2)

# Verificar URL atual
print(f"URL atual: {page.url}")

# Tentar navegar para Dimensions
print("\nNavegando para /app/dimensions...")
page.goto("https://qbo.intuit.com/app/dimensions")
time.sleep(3)

# Verificar se carregou
current_url = page.url
print(f"URL após navegação: {current_url}")

# Capturar screenshot
if "404" not in page.content().lower() and "error" not in current_url.lower():
    filename = generate_filename("TCO", "Dimensions", "DimensionAssignment")
    filepath = capture_screenshot(page, filename)
    print(f"Screenshot salvo: {filepath}")

    # Verificar conteúdo da página
    content = page.content()
    if "dimension" in content.lower():
        print("✓ Página de Dimensions carregada com sucesso!")

        # Procurar elementos relevantes
        if "Dimension Assignment" in content or "assignment" in content.lower():
            print("✓ Dimension Assignment encontrado!")
        if "class" in content.lower() or "location" in content.lower():
            print("✓ Classes/Locations encontrados (são Dimensions)")
else:
    print("✗ Página não carregou corretamente")
    # Tentar via Settings
    print("\nTentando via Settings > Company...")
    page.goto("https://qbo.intuit.com/app/settings")
    time.sleep(2)

    filename = generate_filename("TCO", "Settings", "MainPage")
    filepath = capture_screenshot(page, filename)
    print(f"Screenshot Settings: {filepath}")

pw.stop()
print("\nScript finalizado.")
