"""
Marketing Standup Agent
Generates a daily progress report for the Chairman via Telegram.
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.append("/mnt/HC_Volume_104325311/cli")

from mumega.core.river_engine import RiverEngine
from mumega.core.message import Message, MessageSource

async def generate_standup():
    engine = RiverEngine()
    prompt = "You are Starling, COO. Provide a brief Daily Standup report for Chairman Hadi. Context: Backlog cleared, Marketing HQ active."
    msg = Message(text=prompt, user_id="starling_exec", source=MessageSource.SYSTEM)
    resp = await engine.process_message(msg, skip_tools=True)
    if resp.success:
        report_dir = Path("/mnt/HC_Volume_104325311/mumega-marketing/reports")
        report_dir.mkdir(exist_ok=True)
        report_file = report_dir / f"standup_{datetime.now().strftime("%Y%m%d")}.md"
        report_file.write_text(resp.text)
        print(f"REPORT_SAVED: {report_file}")
        return resp.text

if __name__ == "__main__":
    asyncio.run(generate_standup())
