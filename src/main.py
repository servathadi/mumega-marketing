"""
Marketing Guild - Robust Main Loop
Designed for Render. Stays alive even if credentials are missing.
"""

import time
import schedule
import logging
import sys
import os
import http.server
import threading

# Ensure path
sys.path.append("/app")

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("marketing_guild")

def job_daily_standup():
    logger.info("📢 Check: Triggering Daily Standup...")
    if not os.getenv("GEMINI_API_KEY"):
        logger.warning("❌ Standup aborted: GEMINI_API_KEY missing.")
        return
    try:
        from src.agents.marketing_standup import generate_standup
        import asyncio
        asyncio.run(generate_standup())
        logger.info("✅ Standup transmission successful.")
    except Exception as e:
        logger.error(f"❌ Standup failed: {e}")

def start_health_check_server():
    """Simple server to satisfy Render's port requirement if needed"""
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("", port), handler)
    logger.info(f"Health check server active on port {port}")
    httpd.serve_forever()

def startup():
    logger.info("🚀 Marketing Guild Agent Initializing on Render...")
    
    # Start health check server in background thread
    threading.Thread(target=start_health_check_server, daemon=True).start()
    
    # 1. Verify GitHub App Auth
    app_id = os.getenv("GITHUB_APP_ID")
    private_key = os.getenv("GITHUB_PRIVATE_KEY")
    if app_id and private_key:
        logger.info(f"🔑 Identity Detected: GitHub App {app_id}")
    else:
        logger.warning("⚠️ GitHub App Credentials missing. Push-to-Git disabled.")

    # 2. Schedule Rituals
    # Daily check for standup
    schedule.every(1).hours.do(job_daily_standup)
    
    # Keep-alive heartbeat
    schedule.every(10).minutes.do(lambda: logger.info("❤️ Heartbeat: System Coherent"))

    # Try initial standup, but don't crash if it fails
    job_daily_standup()

    logger.info("📡 Guild entered long-running state.")
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logger.error(f"Loop error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    startup()