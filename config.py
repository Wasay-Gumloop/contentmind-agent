"""
ContentMind AI — Configuration
All settings loaded from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


class Config:
    # ── Identity ───────────────────────────────────────────────
    BRAND_NAME  = os.getenv("BRAND_NAME",  "Ashmeet")
    NICHE       = os.getenv("NICHE",       "AI, Business, Innovation, Psychology")
    AUTHOR_NAME = os.getenv("AUTHOR_NAME", "Ashmeet")
    AUTHOR_BIO  = os.getenv("AUTHOR_BIO",  "Building in public at 14. AI · Business · Innovation.")
    SIGNATURE   = os.getenv("SIGNATURE",   "Built Different. Built Deliberately.")
    TIMEZONE    = os.getenv("TIMEZONE",    "Asia/Kolkata")

    # ── AI Keys ────────────────────────────────────────────────
    OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY",    "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY",    "")
    AI_MODEL          = os.getenv("AI_MODEL",          "gpt-4o")
    AI_FALLBACK_MODEL = os.getenv("AI_FALLBACK_MODEL", "gpt-4o-mini")

    # ── Instagram ──────────────────────────────────────────────
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    INSTAGRAM_ACCOUNT_ID   = os.getenv("INSTAGRAM_ACCOUNT_ID",   "")

    # ── YouTube ────────────────────────────────────────────────
    YOUTUBE_CLIENT_ID      = os.getenv("YOUTUBE_CLIENT_ID",      "")
    YOUTUBE_CLIENT_SECRET  = os.getenv("YOUTUBE_CLIENT_SECRET",  "")
    YOUTUBE_REFRESH_TOKEN  = os.getenv("YOUTUBE_REFRESH_TOKEN",  "")
    YOUTUBE_CHANNEL_ID     = os.getenv("YOUTUBE_CHANNEL_ID",     "")

    # ── Twitter/X ──────────────────────────────────────────────
    TWITTER_API_KEY             = os.getenv("TWITTER_API_KEY",             "")
    TWITTER_API_SECRET          = os.getenv("TWITTER_API_SECRET",          "")
    TWITTER_ACCESS_TOKEN        = os.getenv("TWITTER_ACCESS_TOKEN",        "")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")

    # ── Notion ─────────────────────────────────────────────────
    NOTION_TOKEN       = os.getenv("NOTION_TOKEN",       "")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")

    # ── Research ───────────────────────────────────────────────
    SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
    NEWS_API_KEY   = os.getenv("NEWS_API_KEY",   "")

    # ── Behaviour ──────────────────────────────────────────────
    DRY_RUN      = os.getenv("DRY_RUN", "false").lower() == "true"
    MAX_RETRIES  = int(os.getenv("MAX_RETRIES", "3"))
    CONTENT_TONE = os.getenv("CONTENT_TONE", "confident, direct, ambitious, authentic")

    # ── Paths ──────────────────────────────────────────────────
    ROOT_DIR   = Path(__file__).parent
    MEMORY_DIR = ROOT_DIR / "memory"
    OUTPUT_DIR = ROOT_DIR / "output"
    LOGS_DIR   = ROOT_DIR / "logs"

    # ── Posting Schedule (IST) ─────────────────────────────────
    SCHEDULE = {
        "instagram" : {"days": ["Mon","Wed","Fri","Sun"], "time": "19:00"},
        "youtube"   : {"days": ["Tue","Thu","Sat"],       "time": "18:00"},
        "twitter"   : {"days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], "time": "09:00"},
        "email"     : {"days": ["Tue","Fri"],             "time": "08:00"},
    }

    @classmethod
    def validate(cls):
        warnings = []
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            warnings.append("⚠️  No AI key — set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        if not cls.INSTAGRAM_ACCESS_TOKEN:
            warnings.append("⚠️  INSTAGRAM_ACCESS_TOKEN missing — Instagram posting disabled")
        if not cls.YOUTUBE_REFRESH_TOKEN:
            warnings.append("⚠️  YOUTUBE_REFRESH_TOKEN missing — YouTube posting disabled")
        for w in warnings:
            print(w)
        return len(warnings) == 0
