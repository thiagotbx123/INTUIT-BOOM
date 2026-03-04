# Feature Checker

<p align="center">
  <img src="docs/assets/logo.png" alt="Feature Checker" width="200">
</p>

<p align="center">
  <strong>Automated health checks and feature validation for demo environments</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#documentation">Documentation</a>
</p>

---

## Overview

Feature Checker is an automated validation framework that ensures demo environments are always ready. It logs into applications, navigates to features, validates they work, captures evidence, and alerts when something breaks.

**Problem it solves:** API keys expire, features break, data disappears — and nobody knows until a customer demo fails. Feature Checker catches these issues in minutes, not days.

## Features

- **🔐 Auto Login** — Handles OAuth, MFA/TOTP, session management
- **🧭 Smart Navigation** — Declarative routing with fallbacks
- **📸 Evidence Capture** — Screenshots with annotations
- **✅ Validation Engine** — Check elements, data, API responses
- **🛡️ Content Scanner** — Bilingual profanity/gaffe/PII shield for demo safety
- **🔔 Alerting** — Slack, email, webhooks on failure
- **📊 Reporting** — Excel/JSON reports with history
- **⏰ Scheduling** — Run daily, hourly, or on-demand

## Quick Start

### Prerequisites

- Python 3.9+
- Chrome browser
- Playwright

### Installation

```bash
# Clone the repository
git clone https://github.com/thiagotbx123/tbx-feature-checker.git
cd tbx-feature-checker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### First Run

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Then run:
python -m feature_checker run --product qbo --project TCO
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FEATURE CHECKER                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     │
│  │ Config  │ → │  Auth   │ → │Navigate │ → │Validate │     │
│  │ (JSON)  │   │ (Login) │   │ (Route) │   │ (Check) │     │
│  └─────────┘   └─────────┘   └─────────┘   └────┬────┘     │
│                                                  │          │
│                              ┌────────────────────┤          │
│                              ▼                    ▼          │
│                    ┌─────────────────┐  ┌────────────────┐  │
│                    │    Reporter     │  │Content Scanner │  │
│                    │ (Screenshot +   │  │ (Profanity,    │  │
│                    │  Spreadsheet)   │  │  PII, Gaffes)  │  │
│                    └────────┬────────┘  └────────────────┘  │
│                             │                               │
│                    ┌────────▼────────┐                      │
│                    │    Alerter      │                      │
│                    │ (Slack/Email)   │                      │
│                    └─────────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### Product Configuration

Define your product in `config/products/`:

```json
{
  "name": "QBO",
  "base_url": "https://qbo.intuit.com",
  "auth": {
    "type": "oauth_totp",
    "login_url": "/login"
  },
  "projects": {
    "TCO": {
      "companies": ["Apex", "Global Tread", "Traction"]
    }
  }
}
```

### Health Checks

Define checks in `config/checks/`:

```json
{
  "product": "QBO",
  "checks": [
    {
      "id": "login-works",
      "name": "Login Works",
      "type": "auth",
      "priority": "critical",
      "expect": {
        "url_contains": "/homepage"
      }
    },
    {
      "id": "customers-exist",
      "name": "Customers Have Data",
      "type": "navigation",
      "priority": "high",
      "route": "/app/customers",
      "expect": {
        "selector": "[data-testid='customer-row']",
        "min_count": 1
      }
    }
  ]
}
```

## CLI Reference

```bash
# Run all checks for a product
feature-checker run --product qbo

# Run specific project
feature-checker run --product qbo --project TCO

# Run single check
feature-checker run --product qbo --check login-works

# Dry run (no screenshots, no alerts)
feature-checker run --product qbo --dry-run

# Generate report only
feature-checker report --product qbo --format excel

# List available checks
feature-checker list --product qbo
```

## Check Types

| Type | Description | Example |
|------|-------------|---------|
| `auth` | Validate login works | Login → expect homepage |
| `navigation` | Navigate and validate | Go to page → check element exists |
| `content_scan` | Scan page for profanity/PII/gaffes | Navigate → scan text → flag violations |
| `api` | Call API endpoint | GET /health → expect 200 |
| `data` | Validate data exists | Query → expect count >= N |
| `ui` | Check UI element | Find element → validate text |

## Alerting

Configure alerts in `.env`:

```env
# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
SLACK_CHANNEL=#demo-health

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
ALERT_EMAIL=team@company.com
```

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](docs/getting-started.md) | Installation and first run |
| [Configuration](docs/configuration.md) | Product and check setup |
| [Adding Checks](docs/adding-checks.md) | How to add new checks |
| [Architecture](docs/architecture.md) | System design |
| [API Reference](docs/api-reference.md) | Module documentation |

## Project Structure

```
tbx-feature-checker/
├── src/feature_checker/
│   ├── cli.py              # Command-line interface
│   ├── core/
│   │   ├── checker.py      # Main check orchestrator
│   │   ├── browser.py      # Browser management
│   │   ├── content_scanner.py  # Profanity/PII/gaffe detection
│   │   └── reporter.py     # Report generation
│   ├── auth/
│   │   ├── login.py        # Login handlers
│   │   └── totp.py         # TOTP generation
│   ├── navigation/
│   │   └── navigator.py    # Page navigation
│   └── utils/
│       ├── screenshot.py   # Screenshot capture
│       └── config.py       # Configuration loader
├── config/
│   ├── checks/             # Check definitions
│   └── products/           # Product configurations
├── docs/                   # Documentation
├── examples/               # Usage examples
└── tests/                  # Test suite
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ by TestBox TSA Team
</p>
