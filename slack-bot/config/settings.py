"""
Slack Bot Configuration
"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "knowledge-base"
INTUIT_BOOM_PATH = PROJECT_ROOT

# Slack credentials (set via environment variables)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # xoxb-...
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # xapp-...
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

# Your Slack user ID (bot will only respond when YOU are mentioned)
MY_SLACK_USER_ID = os.getenv("MY_SLACK_USER_ID")  # U0XXXXXXX

# Channels to monitor (leave empty to monitor all)
MONITORED_CHANNELS = os.getenv("MONITORED_CHANNELS", "").split(",")

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Bot behavior
REVIEW_BEFORE_POST = True  # Always review before posting
SEND_REVIEW_AS_DM = True  # Send review to DM instead of thread
