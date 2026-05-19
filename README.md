# ContentMind AI - Autonomous Content Agent

Built by Ashmeet | Built Different. Built Deliberately.

A fully autonomous AI agent that researches trending topics, writes content across every platform, generates cinematic video prompts, and posts to Instagram, YouTube, Twitter, and Notion every single day on autopilot.

## What This Agent Does

| Step | Action | Module |
|------|--------|--------|
| Research | Finds trending topics via Serper + NewsAPI | researcher.py |
| Decide | Picks best topic using virality + history | brain.py |
| Write | Creates 5 content pieces in parallel | writer.py |
| Visualize | Generates AI image + video prompts | visual_engine.py |
| Post | Posts to Instagram, YouTube, Twitter | poster.py |
| Remember | Saves everything, learns over time | memory.py |

## Quick Start

**1. Clone**
```bash
git clone https://github.com/Wasay-Gumloop/contentmind-agent.git
cd contentmind-agent
```

**2. Install**
```bash
pip install -r requirements.txt
```

**3. Configure**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

**4. Run**
```bash
# Full autonomous daily pipeline
python main.py --mode daily

# Single tasks
python main.py --mode blog      --topic "GPT-5 just changed everything"
python main.py --mode youtube   --topic "How to build an AI startup at 14"
python main.py --mode instagram --topic "Morning routine of a young builder"
python main.py --mode twitter   --topic "Why Gen Z will own the future"
python main.py --mode calendar
python main.py --mode video     --topic "AI news this week"

# Test without posting
python main.py --mode daily --dry-run
```

## Architecture

```
contentmind-agent/
|-- main.py                  Entry point + CLI
|-- config.py                All settings from .env
|-- modules/
|   |-- agent_core.py        Master orchestrator
|   |-- researcher.py        Trending topic discovery (Serper + NewsAPI)
|   |-- writer.py            AI content writer - all formats
|   |-- visual_engine.py     Image + video prompt generator
|   |-- poster.py            Platform posting (IG, YT, Twitter, Notion)
|   |-- brain.py             Decision making + learning
|   |-- memory.py            Persistent memory + run history
|   |-- scheduler.py         30-day calendar builder
|   `-- logger.py            Structured logging
|-- .github/workflows/
|   `-- daily_agent.yml      GitHub Actions - runs daily 6AM IST
|-- memory/                  Agent memory (auto-created)
|-- output/                  Generated content (auto-created)
|-- logs/                    Log files (auto-created)
|-- .env.example             Environment variables template
`-- requirements.txt
```

## GitHub Actions - Fully Automated

The agent runs every day at 6:00 AM IST via GitHub Actions - no server needed.

### Setup Secrets
Go to: Settings - Secrets and variables - Actions - New repository secret

| Secret | Get it from |
|--------|-------------|
| OPENAI_API_KEY | platform.openai.com/api-keys |
| INSTAGRAM_ACCESS_TOKEN | Meta for Developers |
| INSTAGRAM_ACCOUNT_ID | Meta Business Suite |
| YOUTUBE_REFRESH_TOKEN | Google Cloud Console |
| TWITTER_API_KEY | developer.twitter.com |
| NOTION_TOKEN | notion.so/my-integrations |
| SERPER_API_KEY | serper.dev - 2500 free searches |
| NEWS_API_KEY | newsapi.org - 100 free/day |

### Manual Trigger
Go to Actions tab - ContentMind AI - Run workflow - pick mode + topic

## Platform Support

| Platform | Write | Post | Notes |
|----------|-------|------|-------|
| Blog | Yes | - | Saved to output/ + Notion |
| Instagram | Yes | Yes | Graph API |
| YouTube | Yes | Yes | Community posts + video upload |
| Twitter/X | Yes | Yes | Full thread |
| Email | Yes | - | Full nurture sequences |
| Notion | Yes | Yes | All content auto-saved |

## Free AI Video Tools

| Tool | Free Tier | Best For |
|------|-----------|----------|
| LTX Video - ltx2video.org | Free credits | 4K 9:16 and 16:9 |
| RunwayML Gen-4 - runwayml.com | 125 credits | Premium cinematic |
| Pika Labs - pika.art | 150/month | Fast Reels |
| Kling AI - klingai.com | 66/day | Storytelling |
| Leonardo AI - leonardo.ai | 150/day | Photorealistic stills |

## Agent Learning

The agent gets smarter over time:
- Stores every run in memory/history.json
- Tracks which topics performed best
- Avoids repeating recent topics
- Adjusts strategy based on results

## License

MIT - Free to use, fork, and build on.

Built by Ashmeet | Building in public at 14 | Built Different. Built Deliberately.
