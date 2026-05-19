# ContentMind AI - Content Writer
# Writes Blog, YouTube Script, Instagram, Twitter Thread, Email, Calendar
# Uses GPT-4o or Claude Anthropic

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
from config import Config

logger = logging.getLogger('ContentMind.Writer')


def get_ai_client():
    if Config.OPENAI_API_KEY:
        from openai import AsyncOpenAI
        return AsyncOpenAI(api_key=Config.OPENAI_API_KEY), 'openai'
    elif Config.ANTHROPIC_API_KEY:
        import anthropic
        return anthropic.AsyncAnthropic(api_key=Config.ANTHROPIC_API_KEY), 'anthropic'
    raise ValueError('No AI key. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env')


async def ai_write(prompt, system=None, max_tokens=2000):
    client, provider = get_ai_client()
    sys_msg = system or (
        'You are ContentMind AI, a world-class content strategist for ' + Config.BRAND_NAME + '. '
        'Niche: ' + Config.NICHE + '. Tone: ' + Config.CONTENT_TONE + '. '
        'Bio: ' + Config.AUTHOR_BIO + '. Every piece must stop the scroll and drive action.'
    )
    try:
        if provider == 'openai':
            r = await client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': prompt}],
                max_tokens=max_tokens, temperature=0.8)
            return r.choices[0].message.content.strip()
        else:
            r = await client.messages.create(
                model='claude-3-5-sonnet-20241022', max_tokens=max_tokens,
                system=sys_msg, messages=[{'role': 'user', 'content': prompt}])
            return r.content[0].text.strip()
    except Exception as e:
        logger.error('AI write failed: ' + str(e))
        return '[ERROR: ' + str(e) + ']'


class ContentWriter:

    async def write_full_package(self, topic):
        logger.info('Writing full package: ' + topic['title'])
        results = await asyncio.gather(
            self.write_blog(topic), self.write_youtube_script(topic),
            self.write_instagram(topic), self.write_twitter_thread(topic),
            self.write_email_sequence(topic), return_exceptions=True)
        def s(r, k, d): return r.get(k, d) if isinstance(r, dict) else d
        return {
            'topic': topic['title'],
            'blog': s(results[0], 'content', ''),
            'youtube_script': s(results[1], 'script', ''),
            'instagram_caption': s(results[2], 'caption', ''),
            'instagram_hashtags': s(results[2], 'hashtags', []),
            'twitter_thread': s(results[3], 'tweets', []),
            'email_sequence': s(results[4], 'emails', []),
            'generated_at': datetime.now().isoformat(),
        }

    async def write_blog(self, topic):
        t = topic.get('title', '')
        prompt = (
            'Write a 1500-2000 word SEO blog post about: ' + t + '\n'
            'Include: H1 title, meta description, hook intro, TOC, 5-7 H2 sections, FAQ, CTA\n'
            'Author: ' + Config.AUTHOR_NAME + '. End with: ' + Config.SIGNATURE
        )
        content = await ai_write(prompt, max_tokens=3000)
        return {'content': content, 'meta': {'title': t, 'words': len(content.split())}}

    async def write_youtube_script(self, topic):
        t = topic.get('title', '')
        prompt = (
            'Full YouTube script for: ' + t + '\n'
            'HOOK(0-30s) | CREDIBILITY(30s-1m) | PROMISE | BODY with B-ROLL cues | ENGAGEMENT | CTA\n'
            'Also include: 3 title options, description, 30 tags, thumbnail concept, chapters\n'
            'Creator: ' + Config.AUTHOR_NAME + '. Signature: ' + Config.SIGNATURE
        )
        script = await ai_write(prompt, max_tokens=3000)
        return {'script': script, 'meta': {'topic': t}}

    async def write_instagram(self, topic):
        t = topic.get('title', '')
        prompt = (
            'Complete Instagram post for: ' + t + '\n'
            '1. Hook line under 125 chars\n'
            '2. Body max 2200 chars with storytelling\n'
            '3. Clear CTA\n'
            '4. 30 hashtags: 5 mega + 10 medium + 15 niche\n'
            '5. Reel concept with 5 scenes and AI image prompts\n'
            'Creator: ' + Config.AUTHOR_NAME + '. End: ' + Config.SIGNATURE
        )
        result = await ai_write(prompt, max_tokens=2000)
        hashtags = [w for line in result.split('\n') for w in line.split() if w.startswith('#')]
        return {'caption': result, 'hashtags': hashtags}

    async def write_twitter_thread(self, topic):
        t = topic.get('title', '')
        prompt = (
            'Viral 15-tweet thread about: ' + t + '\n'
            'Tweet 1=hook. Tweets 2-12=one insight each. Tweets 13-14=story. Tweet 15=CTA.\n'
            'Each under 260 chars. Return numbered list: 1/ tweet text'
        )
        result = await ai_write(prompt, max_tokens=1500)
        tweets = []
        for line in result.split('\n'):
            line = line.strip()
            if line and line[0].isdigit():
                for sep in ['/ ', '. ', ': ', ') ']:
                    if sep in line[:4]:
                        t2 = line.split(sep, 1)[-1].strip()
                        if t2:
                            tweets.append(t2)
                        break
        return {'tweets': tweets or [result]}

    async def write_email_sequence(self, topic):
        t = topic.get('title', '')
        prompt = (
            '5-email nurture sequence about: ' + t + '\n'
            'Each email: Subject (3 options), Preview text, Body (Story->Problem->Solution->Proof->CTA), PS line\n'
            'Brand: ' + Config.BRAND_NAME + '. Tone: ' + Config.CONTENT_TONE
        )
        result = await ai_write(prompt, max_tokens=3000)
        return {'emails': [{'body': result}], 'raw': result}

    async def build_content_calendar(self, niche, days=30):
        prompt = (
            str(days) + '-day content calendar for: ' + niche + '\n'
            'Brand: ' + Config.BRAND_NAME + '\n'
            'Format: Day | Date | Platform | Topic | Format | Hook | Best Time IST\n'
            'Add: batch production schedule, repurposing map, monthly KPI targets'
        )
        result = await ai_write(prompt, max_tokens=4000)
        return {'calendar': result, 'days_planned': days}
