# QBO Feature Checker

Automated QA routine for validating QuickBooks Fall Release features.

## Setup

1. Install dependencies:
   ```bash
   pip install -r qbo_checker/requirements.txt
   playwright install chromium
   ```

2. Set Anthropic API key:
   ```bash
   set ANTHROPIC_API_KEY=your_key_here
   ```

3. Ensure Google Drive sync folder exists:
   ```
   G:\Meu Drive\TestBox\QBO-Evidence\
   ```

## Usage

1. First, login to QBO using the login script:
   ```bash
   python intuit_login_v2_4.py
   ```
   Select the account for the project you want to check.

2. Run the feature checker:
   ```bash
   python -m qbo_checker.main
   ```

3. Select a project (TCO, Construction) and wait for checks to complete.

4. Results are saved to:
   - Screenshots: `G:\Meu Drive\TestBox\QBO-Evidence\{date}_{project}_{company}_{feature}.png`
   - Control sheet: `G:\Meu Drive\TestBox\QBO-Evidence\fall_release_control.xlsx`

## Adding Features

Edit `qbo_checker/features.json` to add new features:

```json
{
  "id": "F004",
  "name": "New Feature",
  "projects": ["TCO"],
  "companies": ["Apex"],
  "route": "/app/feature-route",
  "click_path": [
    {"action": "click", "selector": "text=Menu Item"}
  ],
  "validation": {
    "must_exist": [".feature-element"]
  }
}
```
