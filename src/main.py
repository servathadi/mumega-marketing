"""
Marketing Guild - Main Loop
Runs on Render. Orchestrates standups, content generation, and reporting.
"""

import time
import schedule
import logging
import sys
import os

# Ensure path
sys.path.append("/app")

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("marketing_guild")

def job_daily_standup():
    logger.info("📢 Triggering Daily Standup...")
    try:
        from src.agents.marketing_standup import generate_standup
        import asyncio
        asyncio.run(generate_standup())
    except Exception as e:
        logger.error(f"Standup failed: {e}")

def job_weekly_kpi():
    logger.info("📊 Triggering Weekly KPI Report...")
    # Placeholder for KPI logic
    pass

def startup():
    logger.info("🚀 Marketing Guild Agent Starting on Render...")
    
    # 1. Verify GitHub App Auth
    app_id = os.getenv("GITHUB_APP_ID")
    private_key = os.getenv("GITHUB_PRIVATE_KEY")
    if app_id and private_key:
        try:
            from src.utils.github_auth import get_installation_token
            token = get_installation_token(app_id, private_key, "servathadi", "mumega-marketing")
            logger.info("✅ GitHub App Auth Verified. Installation Token acquired.")
        except Exception as e:
            logger.error(f"❌ GitHub App Auth Failed: {e}")
    else:
        logger.warning("⚠️ GitHub App Credentials missing.")

    # 2. Schedule Rituals
    # ... (rest of startup logic)

if __name__ == "__main__":
    startup()
