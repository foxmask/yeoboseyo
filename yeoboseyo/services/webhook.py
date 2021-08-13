# coding: utf-8
"""
   여보세요 Service Mattermost
"""
# std lib
from __future__ import unicode_literals
import httpx
from logging import getLogger
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)


__all__ = ['Webhook']


class Webhook(Service):
    """
        Service Webhook
    """
    async def save_data(self, trigger, entry) -> bool:
        """
        Post a new text on Mattermost
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        status = False
        # check if we have a 'good' title
        content = str("{title} {link}").format(title=entry.title, link=entry.link)
        payload = {'username': 'Yeoboseyo', 'text': content}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(trigger.webhook, json=payload)
                if r.status_code not in (404, 500):
                    status = True
        except ValueError as e:
            logger.error(e)
            status = False
        return status
