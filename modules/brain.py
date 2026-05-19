"""
ContentMind AI — Agent Brain
Decision-making, topic selection, and learning layer.
"""
import logging
from typing import Dict, List
from config import Config

logger = logging.getLogger("ContentMind.Brain")

VIRAL_FRAMEWORKS = {
    "against_the_grain" : "Everyone says {X}. They're wrong. Here's why...",
    "revelation"        : "I tried {thing} for 30 days. Here's what happened...",
    "list"              : "{N} things {category} doesn't tell you about {topic}",
    "story"             : "3 years ago I was {bad_state}. Today {transformation}.",
    "insider"           : "The {industry} secret that {authority} won't tell you",
    "comparison"        : "{A} vs {B} — the real truth after {timeframe}",
}


class AgentBrain:
    """Strategic decision-making and learning module."""

    def __init__(self, memory):
        self.memory = memory
        self.performance_data = memory.load_performance()

    async def pick_best_topic(self, topics: List[Dict]) -> Dict:
        """Select the best topic using virality + history + content gap analysis."""
        if not topics:
            return {"title": f"The future of {Config.NICHE}", "score": 0.5, "source": "fallback"}

        for topic in topics:
            historical_boost = self._get_historical_boost(topic["title"])
            topic["final_score"] = topic.get("score", 0.5) + historical_boost

        best = max(topics, key=lambda t: t.get("final_score", 0))
        best["framework"] = self._select_framework(best["title"])
        best["hook"]      = self._apply_framework(best["title"], best["framework"])

        logger.info(f"Selected: '{best['title']}' (score: {best.get('final_score', 0):.2f})")
        return best

    def generate_series_suggestions(self, topic: Dict) -> List[str]:
        title = topic.get("title", "")
        return [
            f"The 30-day result: deep dive on {title}",
            f"The biggest mistake people make with {title}",
            f"How {title} will change in the next 12 months",
            f"The {title} toolkit: 7 free tools you need",
            f"Why most people fail at {title} (and what actually works)",
        ]

    def _get_historical_boost(self, title: str) -> float:
        if not self.performance_data:
            return 0.0
        keywords = set(title.lower().split())
        for entry in self.performance_data.get("top_performers", []):
            entry_kw = set(str(entry).lower().split())
            if len(keywords & entry_kw) / max(len(keywords), 1) > 0.3:
                return 0.1
        return 0.0

    def _select_framework(self, title: str) -> str:
        return list(VIRAL_FRAMEWORKS.keys())[len(title) % len(VIRAL_FRAMEWORKS)]

    def _apply_framework(self, title: str, framework: str) -> str:
        templates = {
            "against_the_grain" : f"Everyone thinks they understand {title}. They don't.",
            "revelation"        : f"I spent 30 days studying {title}. This changed everything.",
            "list"              : f"7 things about {title} that nobody is talking about.",
            "story"             : f"6 months ago I knew nothing about {title}. Here's where I am now.",
            "insider"           : f"The real truth about {title} that experts won't tell you.",
            "comparison"        : f"I tested every approach to {title}. Here's what actually works.",
        }
        return templates.get(framework, f"Everything you know about {title} is about to change.")
