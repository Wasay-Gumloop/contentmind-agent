"""
ContentMind AI — Agent Memory
Persistent storage for learning, history, and improvement.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from config import Config

logger = logging.getLogger("ContentMind.Memory")


class AgentMemory:
    """Persistent memory — stores runs, performance, and preferences."""

    def __init__(self):
        self.memory_dir = Config.MEMORY_DIR
        self.output_dir = Config.OUTPUT_DIR
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_files()

    async def save_run(self, topic: Dict, content: Dict, results: Dict) -> str:
        run_data = {
            "run_id"     : datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp"  : datetime.now().isoformat(),
            "topic"      : topic,
            "content_keys": list(content.keys()),
            "results"    : results,
            "metrics"    : {
                "blog_words"      : len(content.get("blog", "").split()),
                "ig_chars"        : len(content.get("instagram_caption", "")),
                "twitter_tweets"  : len(content.get("twitter_thread", [])),
                "platforms_posted": sum(1 for r in results.values() if r.get("success")),
            }
        }
        history = self._load_json("history.json")
        history.append(run_data)
        self._save_json("history.json", history)
        output_path = self.output_dir / f"{run_data['run_id']}_{self._slugify(topic.get('title',''))}.json"
        output_path.write_text(json.dumps({"topic": topic, "content": content, "results": results}, indent=2))
        logger.info(f"Run saved: {run_data['run_id']}")
        return str(output_path)

    def save_output(self, content_type: str, content: Any) -> str:
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"{ts}_{content_type}.json"
        path.write_text(json.dumps(content if isinstance(content, dict) else {"content": content}, indent=2))
        text_path = self.output_dir / f"{ts}_{content_type}.txt"
        with open(text_path, "w") as f:
            if isinstance(content, dict):
                for k, v in content.items():
                    f.write(f"\n{'='*50}\n{k.upper()}\n{'='*50}\n")
                    if isinstance(v, list):
                        for i, item in enumerate(v, 1): f.write(f"\n[{i}] {item}\n")
                    else:
                        f.write(f"{v}\n")
            else:
                f.write(str(content))
        logger.info(f"Output saved: {text_path}")
        return str(text_path)

    def save_calendar(self, calendar: Dict) -> str:
        ym = datetime.now().strftime("%Y%m")
        path = self.output_dir / f"calendar_{ym}.txt"
        path.write_text(calendar.get("calendar", ""))
        return str(path)

    def load_performance(self) -> Dict:
        history = self._load_json("history.json")
        if not history: return {}
        successful = [r for r in history if any(v.get("success") for v in r.get("results", {}).values())]
        return {
            "total_runs"      : len(history),
            "successful_runs" : len(successful),
            "top_performers"  : [r["topic"] for r in successful[-5:]],
            "last_run"        : history[-1]["timestamp"] if history else None,
        }

    def total_runs(self) -> List:
        return self._load_json("history.json")

    def get_recent_topics(self, n: int = 10) -> List[str]:
        return [r["topic"].get("title", "") for r in self._load_json("history.json")[-n:]]

    def _ensure_files(self):
        for f in ["history.json", "preferences.json"]:
            p = self.memory_dir / f
            if not p.exists():
                self._save_json(f, [] if "history" in f else {})

    def _load_json(self, filename: str) -> Any:
        path = self.memory_dir / filename
        try:
            return json.loads(path.read_text())
        except Exception:
            return [] if "history" in filename else {}

    def _save_json(self, filename: str, data: Any):
        (self.memory_dir / filename).write_text(json.dumps(data, indent=2))

    def _slugify(self, text: str) -> str:
        return "".join(c if c.isalnum() else "_" for c in text.replace(" ", "_"))[:40]
