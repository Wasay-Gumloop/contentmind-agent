# ContentMind AI - Visual Engine
# Generates AI image prompts, video storyboards, cinematic scenes
# Supports: LTX Video, RunwayML, Pika Labs, Kling AI, Leonardo AI

import logging
import asyncio
from typing import Dict, List
from datetime import datetime
from modules.writer import ai_write
from config import Config

logger = logging.getLogger('ContentMind.VisualEngine')

VIDEO_TOOLS = {
    'ltx':    'LTX Video (ltx2video.org) - Free 4K, 9:16 and 16:9',
    'runway': 'RunwayML Gen-4 (runwayml.com) - 125 free credits',
    'pika':   'Pika Labs (pika.art) - 150 free/month',
    'kling':  'Kling AI (klingai.com) - 66 free credits/day',
    'capcut': 'CapCut AI - free editing + auto-captions',
}

IMAGE_TOOLS = {
    'leonardo': 'Leonardo AI (leonardo.ai) - 150 free credits/day',
    'firefly':  'Adobe Firefly - 25 free/month, commercial license',
    'dalle':    'DALL-E 3 via OpenAI API',
}


class VisualEngine:

    async def generate_prompts(self, topic, content):
        image_prompts, video_scenes, thumbnail = await asyncio.gather(
            self._image_prompts(topic),
            self._video_storyboard(topic),
            self._thumbnail(topic))
        return {
            'image_prompts': image_prompts,
            'video_scenes': video_scenes,
            'thumbnail': thumbnail,
            'tools': {'images': IMAGE_TOOLS, 'videos': VIDEO_TOOLS},
            'generated_at': datetime.now().isoformat()
        }

    async def generate_full_video_package(self, topic):
        t = topic.get('title', '')
        prompt = (
            'Create a CINEMATIC VIDEO PRODUCTION PACKAGE for: ' + t + '\n'
            'Include:\n'
            '- Concept: hook, narrative arc, duration, aspect ratio, style\n'
            '- Full storyboard (8 scenes): visual, duration, camera, AI prompt, text overlay, voiceover\n'
            '- Audio direction: music mood and free sources\n'
            '- Platform versions: YouTube 16:9 notes + Instagram Reels 9:16 notes\n'
            '- Tool guide: which scenes to generate in LTX Video vs RunwayML vs Pika\n'
            'Creator: ' + Config.AUTHOR_NAME
        )
        package = await ai_write(prompt, max_tokens=3000)
        return {'package': package, 'topic': t}

    async def _image_prompts(self, topic):
        t = topic.get('title', '')
        prompt = (
            'Generate 5 cinematic AI image prompts for content about: ' + t + '\n'
            'Style: dark ambitious, teal and amber color grade, ARRI Alexa 4K, photorealistic.\n'
            'Format each: [shot type], [subject], [environment], [lighting], [camera], [color grade]\n'
            'Number 1-5 with purpose label (cover/Instagram/thumbnail etc). No text in images.'
        )
        result = await ai_write(prompt, max_tokens=600)
        prompts = []
        for i, line in enumerate(result.split('\n'), 1):
            if line.strip() and line.strip()[0].isdigit():
                prompts.append({
                    'id': i,
                    'prompt': line.strip(),
                    'tool': 'Leonardo AI - 150 free credits/day',
                    'ratio': '16:9'
                })
        return prompts[:5] or [{'id': 1, 'prompt': result, 'tool': 'Leonardo AI'}]

    async def _video_storyboard(self, topic):
        t = topic.get('title', '')
        prompt = (
            '6-scene video storyboard for: ' + t + '\n'
            'For each scene provide:\n'
            'Scene: [N] | Visual: [description] | Duration: [Xs] | Camera: [movement]\n'
            'Prompt: [AI video generation prompt] | Text: [on-screen overlay] | VO: [voiceover line]'
        )
        result = await ai_write(prompt, max_tokens=1200)
        scenes, cur = [], {}
        for line in result.split('\n'):
            line = line.strip()
            if line.lower().startswith('scene'):
                if cur:
                    scenes.append(cur)
                cur = {'scene': line}
            elif ':' in line and cur:
                k, v = line.split(':', 1)
                cur[k.strip().lower()] = v.strip()
        if cur:
            scenes.append(cur)
        return scenes or [{'prompt': result}]

    async def _thumbnail(self, topic):
        t = topic.get('title', '')
        prompt = (
            'YouTube thumbnail concept for: ' + t + '\n'
            'Provide: main visual element, bold text (max 6 words),\n'
            'color scheme (teal and amber), emotional trigger, AI prompt to generate it.'
        )
        result = await ai_write(prompt, max_tokens=350)
        return {'concept': result}
