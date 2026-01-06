"""
Marketing Guild - Robust Main Loop
Designed for Render. Runs Agent Loop AND serves Landing Page.
"""

import time
import schedule
import logging
import sys
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Ensure path
sys.path.append("/app")

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("marketing_guild")

# Path to the Landing Page
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

class LandingPageHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Read and serve the template
            index_path = os.path.join(TEMPLATE_DIR, "index.html")
            if os.path.exists(index_path):
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>Mumega Marketing HQ</h1><p>Agent Active. Landing page not found.</p>")
        else:
            # Basic 404 for now
            self.send_error(404)

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

def start_web_server():
    """Serves the Landing Page on the PORT"""
    port = int(os.environ.get("PORT", 10000))
    # Change directory to src so we can find templates if needed relative
    # os.chdir("/app/src") 
    
    server = HTTPServer(("0.0.0.0", port), LandingPageHandler)
    logger.info(f"🌐 Web Server active on port {port}")
    server.serve_forever()

def startup():
    logger.info("🚀 Marketing Guild Agent Initializing on Render...")
    
    # Start Web Server in background thread (Daemon)
    # This allows Render to bind the port and keeps the service healthy
    threading.Thread(target=start_web_server, daemon=True).start()
    
    # 1. Verify GitHub App Auth
    app_id = os.getenv("GITHUB_APP_ID")
    if app_id:
        logger.info(f"🔑 Identity Detected: GitHub App {app_id}")
    else:
        logger.warning("⚠️ GitHub App Credentials missing.")

    # 2. Schedule Rituals
    schedule.every(1).hours.do(job_daily_standup)
    schedule.every(10).minutes.do(lambda: logger.info("❤️ Heartbeat: System Coherent"))

    # Initial check
    # job_daily_standup() # Commented out to prevent crash loop on start if keys missing

    logger.info("📡 Guild entered long-running state.")
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logger.error(f"Loop error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    startup()
