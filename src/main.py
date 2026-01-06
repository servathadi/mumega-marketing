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
    
    # Check Env Vars
    if not os.getenv("GEMINI_API_KEY"):
        logger.warning("⚠️ GEMINI_API_KEY not found. Brain function limited.")
    
    # Schedule Rituals
    # Standup at 9:00 AM UTC (adjust as needed)
    schedule.every().day.at("09:00").do(job_daily_standup)
    
    # Keep-alive heartbeat (logs every hour)
    schedule.every(1).hours.do(lambda: logger.info("❤️ Guild Heartbeat: Active"))

    # Immediate check on startup
    job_daily_standup()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    startup()
