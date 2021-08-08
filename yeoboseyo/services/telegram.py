# coding: utf-8
"""
   여보세요 Service Telegram
"""
# std lib
from __future__ import unicode_literals
import httpx
from logging import getLogger
# starlette
from starlette.config import Config

# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['Telegram']


class Telegram(Service):
    """
        Service Telegram
    """

    def __init__(self):
        self.token = config('TELEGRAM_TOKEN')

    async def save_data(self, trigger, entry) -> bool:
        """
        Post a new text on Telegram in markdown format
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        status = False
        content = str("[{title}]({link}) [{link}]({link})").format(title=entry.title, link=entry.link)
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {'chat_id': config('TELEGRAM_CHAT_ID'),
                   'text': content,
                   'parse_mode': 'markdown'}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload)
                if r.status_code == 200:
                    status = True
        except ValueError as e:
            logger.error(e)
            status = False
        return status
