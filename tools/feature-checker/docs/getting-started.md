# Getting Started

This guide will help you set up and run your first health checks.

## Prerequisites

- Python 3.9 or higher
- Google Chrome browser
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thiagotbx123/tbx-feature-checker.git
cd tbx-feature-checker
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browser

```bash
playwright install chromium
```

### 5. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit with your settings
# - Add credentials
# - Set paths
# - Configure alerts (optional)
```

## Running Your First Check

### 1. Check Configuration

```bash
python -m feature_checker status
```

This shows if everything is configured correctly.

### 2. List Available Checks

```bash
python -m feature_checker list --product qbo
```

### 3. Run Health Checks

```bash
# Run all checks
python -m feature_checker run --product qbo

# Run specific project
python -m feature_checker run --product qbo --project TCO

# Dry run (no screenshots)
python -m feature_checker run --product qbo --dry-run
```

## Understanding Results

### Status Meanings

| Status | Meaning |
|--------|---------|
| PASS | Check passed successfully |
| FAIL | Check failed - action needed |
| PARTIAL | Check passed with warnings |
| SKIP | Check was skipped |

### Output Files

After running checks, you'll find:

- **Screenshots** in `output/evidence/`
- **Reports** in `output/reports/`

## Next Steps

- [Configuration Guide](configuration.md) - Customize settings
- [Adding Checks](adding-checks.md) - Create custom checks
- [Architecture](architecture.md) - How it works
