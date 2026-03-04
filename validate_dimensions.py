import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Users\adm_r\intuit-boom")

from qbo_checker.login import ensure_logged_in
from qbo_checker.screenshot import capture_screenshot
import time

print("=== Feature 1: Dimensions - Dimension Assignment ===")
print()

pw, browser, page = ensure_logged_in("TCO")
time.sleep(2)

# Navegar para Dimensions via Settings > Dimensions
print("Navegando para Settings > Dimensions...")

# Clicar no icone de Settings (engrenagem)
try:
    page.click('[data-testid="settings-gear"]')
    time.sleep(2)
except Exception:
    # Tentar via URL direta
    print("Tentando via URL direta...")
    page.goto("https://qbo.intuit.com/app/dimensions")
    time.sleep(3)

filepath = capture_screenshot(page, "2025-12-03_TCO_Dimensions_01.png")
print(f"Screenshot 1: {filepath}")

# Verificar se estamos na pagina de Dimensions
current_url = page.url
print(f"URL: {current_url}")

# Se nao estiver em dimensions, tentar All apps
if "dimensions" not in current_url.lower():
    print("Tentando via All apps...")
    page.goto("https://qbo.intuit.com/app/apps")
    time.sleep(3)

    # Buscar Dimensions
    try:
        search = page.locator('input[placeholder*="Search"]').first
        search.fill("Dimensions")
        time.sleep(2)
    except Exception:
        pass

    filepath = capture_screenshot(page, "2025-12-03_TCO_Dimensions_Search.png")
    print(f"Screenshot Search: {filepath}")

print("Done!")
