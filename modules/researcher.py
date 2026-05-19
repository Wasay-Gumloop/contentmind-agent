"""
ContentMind AI — Research Module
Autonomously finds trending topics, viral angles, competitor content.
"""
import httpx
import asyncio
import logging
from datetime import datetime
from typing import List, Dict
from config import Config

logger = logging.getLogger("ContentMind.Researcher")


class Researcher:
    """Autonomous research engine using Serper, NewsAPI, and smart fallbacks."""

    def __init__(self):
        self.serper_key = Config.SERPER_API_KEY
        self.news_key   = Config.NEWS_API_KEY

    async def get_trending_topics(self, niche: str, count: int = 5) -> List[Dict]:
        """Research trending topics in the niche."""
        logger.info(f"Researching topics: {niche}")
        topics = []
        if self.serper_key:
            topics += await self._search_serper(niche)
        if self.news_key:
            topics += await self._search_news(niche)
        if not topics:
            topics = self._get_seed_topics(niche)
        unique = self._dedupe(topics)
        ranked = self._rank_by_virality(unique)
        return ranked[:count]

    async def get_topic_details(self, topic: str) -> Dict:
        """Get deep research on a specific topic."""
        return {
            "title"    : topic,
            "keywords" : self._extract_keywords(topic),
            "angle"    : self._suggest_angle(topic),
            "hook"     : self._generate_hook(topic),
            "timestamp": datetime.now().isoformat(),
        }

    async def _search_serper(self, query: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    "https://google.serper.dev/search",
                    headers={"X-API-KEY": self.serper_key, "Content-Type": "application/json"},
                    json={"q": f"{query} trending 2026", "num": 10}
                )
                return [{
                    "title"  : item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url"    : item.get("link", ""),
                    "source" : "serper",
                    "score"  : 0.8,
                } for item in r.json().get("organic", [])[:5]]
        except Exception as e:
            logger.warning(f"Serper failed: {e}")
            return []

    async def _search_news(self, query: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    "https://newsapi.org/v2/everything",
                    params={"q": query, "sortBy": "publishedAt", "language": "en",
                            "pageSize": 5, "apiKey": self.news_key}
                )
                return [{
                    "title"  : a["title"],
                    "snippet": a.get("description", ""),
                    "url"    : a["url"],
                    "source" : "newsapi",
                    "score"  : 0.7,
                } for a in r.json().get("articles", []) if a.get("title")]
        except Exception as e:
            logger.warning(f"NewsAPI failed: {e}")
            return []

    def _get_seed_topics(self, niche: str) -> List[Dict]:
        seeds = [
            {"title": "GPT-5.5 can now control your computer — what this changes", "score": 0.95},
            {"title": "5 AI tools that will save you 10 hours this week", "score": 0.90},
            {"title": "Why every 14-year-old should learn AI right now", "score": 0.88},
            {"title": "Google DeepMind reinvented the mouse — here's why it matters", "score": 0.85},
            {"title": f"The future of {niche} in 2026", "score": 0.75},
        ]
        for s in seeds:
            s["source"] = "seed"
        return seeds

    def _dedupe(self, topics):
        seen, unique = set(), []
        for t in topics:
            key = t["title"].lower()[:50]
            if key not in seen:
                seen.add(key)
                unique.append(t)
        return unique

    def _rank_by_virality(self, topics):
        VIRAL = ["secret","nobody","never","always","first","just","why","how",
                 "changed","revealed","truth","billion","million","hack","best"]
        for t in topics:
            bonus = sum(0.05 for w in VIRAL if w in t["title"].lower())
            t["score"] = t.get("score", 0.5) + bonus
        return sorted(topics, key=lambda x: x["score"], reverse=True)

    def _extract_keywords(self, topic):
        stop = {"the","a","an","is","are","in","of","to","and","for","with","how","why"}
        return [w.lower() for w in topic.split() if w.lower() not in stop][:8]

    def _suggest_angle(self, topic):
        angles = ["against_the_grain","revelation","insider","comparison","story","list"]
        return angles[len(topic) % len(angles)]

    def _generate_hook(self, topic):
        hooks = [
            f"Nobody is talking about this — {topic}",
            f"I spent 30 days studying {topic}. Here's what I found.",
            f"Everyone is wrong about {topic}.",
            f"The {topic} secret that most people miss.",
            f"This changed everything I thought I knew about {topic}.",
        ]
        return hooks[len(topic) % len(hooks)]
