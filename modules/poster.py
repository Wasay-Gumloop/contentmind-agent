# ContentMind AI - Platform Poster
# Direct posting to Instagram, YouTube, Twitter, and Notion

import httpx
import logging
from typing import Dict
from config import Config

logger = logging.getLogger('ContentMind.Poster')


class Poster:

    async def post_all(self, content, visuals):
        if Config.DRY_RUN:
            logger.info('DRY RUN - skipping posts')
            return {p: {'success': True, 'message': 'DRY RUN - content ready'}
                    for p in ['instagram', 'youtube', 'twitter', 'notion']}
        results = {}
        for name, coro in {
            'instagram': self.post_instagram(content),
            'youtube':   self.post_youtube_community(content),
            'twitter':   self.post_twitter_thread(content),
            'notion':    self.save_to_notion(content),
        }.items():
            try:
                results[name] = await coro
            except Exception as e:
                results[name] = {'success': False, 'message': str(e)}
        return results

    async def post_instagram(self, content):
        if not Config.INSTAGRAM_ACCESS_TOKEN:
            return {'success': False, 'message': 'Add INSTAGRAM_ACCESS_TOKEN to .env'}
        caption = content.get('instagram_caption', '')
        tags = ' '.join(content.get('instagram_hashtags', []))
        full = (caption + '\n\n' + tags).strip()
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    'https://graph.instagram.com/' + Config.INSTAGRAM_ACCOUNT_ID + '/media',
                    params={'caption': full, 'image_url': content.get('image_url', ''),
                            'access_token': Config.INSTAGRAM_ACCESS_TOKEN})
                cid = r.json().get('id')
                if not cid:
                    return {'success': False, 'message': str(r.json())}
                r2 = await c.post(
                    'https://graph.instagram.com/' + Config.INSTAGRAM_ACCOUNT_ID + '/media_publish',
                    params={'creation_id': cid, 'access_token': Config.INSTAGRAM_ACCESS_TOKEN})
                res = r2.json()
                if res.get('id'):
                    return {'success': True, 'message': 'Posted! ' + res['id']}
                return {'success': False, 'message': str(res)}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    async def post_youtube_community(self, content):
        if not Config.YOUTUBE_REFRESH_TOKEN:
            return {'success': False, 'message': 'Add YOUTUBE_REFRESH_TOKEN to .env'}
        text = (
            'New: ' + content.get('topic', '') + '\n\n' +
            content.get('blog', '')[:400] + '\n\n' +
            'Drop a fire emoji if this was valuable!\n' +
            '- ' + Config.AUTHOR_NAME + ' | ' + Config.SIGNATURE
        )
        try:
            token = await self._get_yt_token()
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    'https://www.googleapis.com/youtube/v3/communityPosts',
                    headers={'Authorization': 'Bearer ' + token},
                    json={'snippet': {'text': text}})
                res = r.json()
                return {'success': 'id' in res, 'message': res.get('id', str(res))}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    async def post_twitter_thread(self, content):
        tweets = content.get('twitter_thread', [])
        if not tweets:
            return {'success': False, 'message': 'No tweets'}
        if not Config.TWITTER_API_KEY:
            return {'success': False, 'message': 'Add TWITTER_API_KEY to .env'}
        try:
            import tweepy
            cl = tweepy.AsyncClient(
                consumer_key=Config.TWITTER_API_KEY,
                consumer_secret=Config.TWITTER_API_SECRET,
                access_token=Config.TWITTER_ACCESS_TOKEN,
                access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET)
            prev_id, count = None, 0
            for tw in tweets[:15]:
                kw = {'text': tw[:280]}
                if prev_id:
                    kw['in_reply_to_tweet_id'] = prev_id
                r = await cl.create_tweet(**kw)
                prev_id = r.data['id']
                count += 1
            return {'success': True, 'message': 'Thread posted: ' + str(count) + ' tweets'}
        except ImportError:
            return {'success': False, 'message': 'Run: pip install tweepy'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    async def save_to_notion(self, content):
        if not Config.NOTION_TOKEN:
            return {'success': False, 'message': 'Add NOTION_TOKEN to .env'}
        from datetime import date
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    'https://api.notion.com/v1/pages',
                    headers={
                        'Authorization': 'Bearer ' + Config.NOTION_TOKEN,
                        'Content-Type': 'application/json',
                        'Notion-Version': '2022-06-28'
                    },
                    json={
                        'parent': {'database_id': Config.NOTION_DATABASE_ID},
                        'properties': {
                            'Name':   {'title': [{'text': {'content': content.get('topic', 'Untitled')}}]},
                            'Status': {'select': {'name': 'Published'}},
                            'Date':   {'date': {'start': date.today().isoformat()}}
                        },
                        'children': [{
                            'object': 'block', 'type': 'paragraph',
                            'paragraph': {'rich_text': [{
                                'type': 'text',
                                'text': {'content': content.get('blog', '')[:2000]}
                            }]}
                        }]
                    })
                res = r.json()
                return {'success': 'id' in res, 'message': res.get('id', str(res))}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    async def _get_yt_token(self):
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post('https://oauth2.googleapis.com/token', data={
                'client_id':     Config.YOUTUBE_CLIENT_ID,
                'client_secret': Config.YOUTUBE_CLIENT_SECRET,
                'refresh_token': Config.YOUTUBE_REFRESH_TOKEN,
                'grant_type':    'refresh_token'
            })
            t = r.json().get('access_token')
            if not t:
                raise ValueError('Token refresh failed: ' + str(r.json()))
            return t
