# coding: utf-8
"""
   여보세요 - Service Wallabag
"""

# std lib
from __future__ import unicode_literals

from logging import getLogger
# yeoboseyo
from yeoboseyo import settings
from yeoboseyo.services import Service
# wallabag
from wallabagapi import WallabagAPI

# create logger
logger = getLogger(__name__)


__all__ = ['Wallabag']


class Wallabag(Service):
    """
        Service Wallabag
    """

    async def save_data(self, trigger, entry) -> bool:
        """
        Post a new text on Wallabag
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        status = False
        if trigger.wallabag:
            # get a new token if expired
            token = await WallabagAPI.get_token(host=settings.WALLABAG_URL,
                                                username=settings.WALLABAG_USERNAME,
                                                password=settings.WALLABAG_PASSWORD,
                                                client_id=settings.WALLABAG_CLIENTID,
                                                client_secret=settings.WALLABAG_CLIENTSECRET)
            # then post
            w = WallabagAPI(host=settings.WALLABAG_URL, token=token)

            status = await w.post_entries(url=entry.link)

        return status
