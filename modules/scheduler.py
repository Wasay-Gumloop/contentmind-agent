"""
ContentMind AI — Scheduler
Builds 30-day content calendars and manages autonomous posting schedules.
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from modules.writer import ai_write
from config import Config

logger = logging.getLogger("ContentMind.Scheduler")

PLATFORMS_ROTATION = [
    "Instagram","Twitter","YouTube","Instagram",
    "Twitter","Email","Instagram","Twitter",
    "YouTube","Instagram","Twitter","Instagram",
    "Email","YouTube","Twitter",
]


class Scheduler:
    """Builds and manages autonomous content schedules."""

    async def build_30_day_plan(self, niche: str, brand_name: str) -> Dict:
        logger.info(f"Building 30-day plan for {brand_name}")
        topics  = await self._generate_30_topics(niche)
        days    = self._build_calendar_days(topics)
        batches = self._plan_batch_sessions(days)
        prompt  = f"""
Build a complete 30-day content calendar for {brand_name} ({niche}).
Return a table: Day | Date | Platform | Topic | Format | Best Time IST
Then add: batch production schedule + repurposing map + monthly KPI targets.
Topics: {json.dumps([d['topic'] for d in days[:10]])} ... (and 20 more)
"""
        calendar_text = await ai_write(prompt, max_tokens=3000)
        return {"brand": brand_name, "niche": niche, "days": days,
                "batches": batches, "calendar": calendar_text, "created": datetime.now().isoformat()}

    async def _generate_30_topics(self, niche: str) -> List[str]:
        prompt = f"""
Generate 30 unique, highly engaging content topics for: {niche}
Creator: {Config.AUTHOR_NAME} | {Config.AUTHOR_BIO}
Mix: how-to, story, list, opinion, news, case study, personal growth.
Return as numbered list only.
"""
        result = await ai_write(prompt, max_tokens=1500)
        topics = []
        for line in result.split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                for sep in [". ", ") ", ": "]:
                    if sep in line[:4]:
                        t = line.split(sep, 1)[-1].strip()
                        if t: topics.append(t)
                        break
        return topics[:30] if len(topics) >= 30 else topics + [f"{niche} insight {i}" for i in range(30 - len(topics))]

    def _build_calendar_days(self, topics: List[str]) -> List[Dict]:
        today = datetime.now()
        return [{
            "day"     : i,
            "date"    : (today + timedelta(days=i)).strftime("%b %d, %Y"),
            "platform": PLATFORMS_ROTATION[i % len(PLATFORMS_ROTATION)],
            "topic"   : topic,
            "format"  : self._get_format(PLATFORMS_ROTATION[i % len(PLATFORMS_ROTATION)]),
            "time_ist": Config.SCHEDULE.get(PLATFORMS_ROTATION[i % len(PLATFORMS_ROTATION)].lower(), {}).get("time", "18:00"),
            "status"  : "scheduled",
        } for i, topic in enumerate(topics[:30], 1)]

    def _plan_batch_sessions(self, days: List[Dict]) -> List[Dict]:
        sessions = []
        for i in range(0, len(days), 5):
            batch = days[i:i+5]
            sessions.append({
                "session"  : len(sessions) + 1,
                "pieces"   : len(batch),
                "topics"   : [d["topic"] for d in batch],
                "platforms": list(set(d["platform"] for d in batch)),
                "duration" : "2-3 hours",
            })
        return sessions

    def _get_format(self, platform: str) -> str:
        return {"Instagram": "Carousel/Reel", "YouTube": "Long-form",
                "Twitter": "Thread", "Email": "Newsletter"}.get(platform, "Post")
