"""
Slack Bot Entry Point
Start the bot with: python main.py
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()

# Verify required env vars (ANTHROPIC_API_KEY not needed - using Claude Code CLI)
required_vars = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "MY_SLACK_USER_ID"]

missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"ERROR: Missing environment variables: {missing}")
    print("\nCreate a .env file with:")
    for v in required_vars:
        print(f"  {v}=your_value")
    sys.exit(1)

from src.slack_bot import start_bot

if __name__ == "__main__":
    print("=" * 50)
    print("QBO Support Bot - TestBox (Ollama Local LLM)")
    print("=" * 50)
    print("Backend: Ollama llama3.2")
    print(f"Knowledge base: {Path(__file__).parent.parent / 'knowledge-base'}")
    print(f"Monitoring for mentions of user: {os.getenv('MY_SLACK_USER_ID')}")
    print("=" * 50)
    start_bot()
