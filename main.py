#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        ContentMind AI — Autonomous Content Agent             ║
║        Built by Ashmeet | Built Different. Built Deliberately║
║        Version: 2.0.0 | Fully Autonomous                     ║
╚══════════════════════════════════════════════════════════════╝

This agent autonomously:
  → Researches trending topics daily
  → Writes blogs, YouTube scripts, Instagram captions,
    Twitter threads, and email sequences
  → Generates AI image & video prompts
  → Posts directly to Instagram & YouTube
  → Schedules a full 30-day content calendar
  → Learns from performance data over time
"""

import asyncio
import argparse
import logging
from datetime import datetime
from modules.agent_core import ContentMindAgent
from modules.logger import setup_logger
from config import Config

logger = setup_logger("ContentMind", "logs/agent.log")


async def run_daily_pipeline(agent: ContentMindAgent):
    """Full autonomous daily content pipeline."""
    logger.info("Starting Daily Content Pipeline")
    print("\n" + "="*60)
    print(f"  🧠 ContentMind AI — {datetime.now().strftime('%A, %B %d %Y — %I:%M %p')}")
    print("="*60 + "\n")

    print("🔍 [1/6] Researching trending topics...")
    topics = await agent.researcher.get_trending_topics(niche=Config.NICHE, count=5)
    print(f"   ✅ Found {len(topics)} trending topics")

    best = await agent.brain.pick_best_topic(topics)
    print(f"\n🎯 [2/6] Topic: '{best['title']}'")

    print("\n✍️  [3/6] Writing all content...")
    content = await agent.writer.write_full_package(best)
    print(f"   ✅ Blog: {len(content['blog'].split())} words")
    print(f"   ✅ YouTube script: {len(content['youtube_script'].split())} words")
    print(f"   ✅ Instagram: {len(content['instagram_caption'])} chars")
    print(f"   ✅ Twitter: {len(content['twitter_thread'])} tweets")

    print("\n🎨 [4/6] Generating visual & video prompts...")
    visuals = await agent.visual_engine.generate_prompts(best, content)
    print(f"   ✅ {len(visuals['image_prompts'])} image + {len(visuals['video_scenes'])} video prompts")

    print("\n📤 [5/6] Posting to platforms...")
    results = await agent.poster.post_all(content, visuals)
    for platform, r in results.items():
        status = "✅" if r["success"] else "⚠️ "
        print(f"   {status} {platform}: {r['message']}")

    print("\n🧠 [6/6] Saving to memory...")
    await agent.memory.save_run(best, content, results)

    posted = sum(1 for r in results.values() if r["success"])
    print(f"\n{'='*60}")
    print(f"  ✅ PIPELINE COMPLETE | Topic: {best['title']}")
    print(f"  📤 Posted to {posted}/{len(results)} platforms")
    print("="*60 + "\n")
    return {"topic": best, "content": content, "results": results}


async def run_single(agent, task: str, topic: str = None):
    """Run a single content task on demand."""
    topic = topic or f"Latest trends in {Config.NICHE}"
    t = {"title": topic, "keywords": [], "score": 0.8}
    print(f"\n🎯 Running: {task} | Topic: {topic}\n")

    handlers = {
        "blog"      : lambda: agent.writer.write_blog(t),
        "youtube"   : lambda: agent.writer.write_youtube_script(t),
        "instagram" : lambda: agent.writer.write_instagram(t),
        "twitter"   : lambda: agent.writer.write_twitter_thread(t),
        "email"     : lambda: agent.writer.write_email_sequence(t),
        "calendar"  : lambda: agent.writer.build_content_calendar(topic, days=30),
        "video"     : lambda: agent.visual_engine.generate_full_video_package(t),
    }
    if task not in handlers:
        print(f"Unknown task: {task}")
        return
    result = await handlers[task]()
    agent.memory.save_output(task, result)
    # Print the most useful key
    for key in ["content", "script", "caption", "calendar", "package"]:
        if key in result:
            print(result[key])
            break
    if task == "twitter" and "tweets" in result:
        for i, tw in enumerate(result["tweets"], 1):
            print(f"[{i}] {tw}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ContentMind AI — Autonomous Content Agent",
        epilog="""
Examples:
  python main.py --mode daily
  python main.py --mode blog --topic "GPT-5 changed everything"
  python main.py --mode youtube --topic "How to build an AI startup at 14"
  python main.py --mode instagram --topic "Morning mindset habits"
  python main.py --mode twitter --topic "Why Gen Z will own the future"
  python main.py --mode calendar
  python main.py --mode video --topic "AI news this week"
  python main.py --mode daily --dry-run
        """
    )
    parser.add_argument("--mode", default="daily",
        choices=["daily","blog","youtube","instagram","twitter","email","calendar","video"])
    parser.add_argument("--topic",   type=str, default=None)
    parser.add_argument("--niche",   type=str, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.niche:   Config.NICHE    = args.niche
    if args.dry_run: Config.DRY_RUN  = True

    agent = ContentMindAgent()

    if args.mode == "daily":
        asyncio.run(run_daily_pipeline(agent))
    else:
        asyncio.run(run_single(agent, args.mode, args.topic))


if __name__ == "__main__":
    main()
