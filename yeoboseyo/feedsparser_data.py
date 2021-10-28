# coding: utf-8
"""
   FeedParserData
"""
# std lib
from __future__ import unicode_literals
from logging import getLogger
import typing
# external lib
import feedparser
import httpx

# create logger
logger = getLogger(__name__)

__author__ = 'FoxMaSk'
__all__ = ['RssAsync']


class RssAsync:

    USER_AGENT = f'FeedParserData/0.1.3 +https://framagit.org/annyong/yeoboseyo'

    async def get_data(self, url_to_parse, bypass_bozo=False, **kwargs) -> typing.Any:
        """
        read the data from a given URL or path to a local file
        :string url_to_parse : URL of the Feed to parse
        :boolean bypass_bozo : for not well formed URL, do we ignore or not that URL
        :return: Feeds if Feeds are well formed
        """
        data = {'bozo': 0, 'entries': []}
        async with httpx.AsyncClient(timeout=30) as client:
            feed = await client.get(url_to_parse)
            logger.debug(url_to_parse)
            if feed.status_code == 200:
                data = feedparser.parse(feed.text, agent=self.USER_AGENT)
                # if the feeds is not well formed, return no data at all
            if bypass_bozo is False and data.bozo == 1:
                data.entries = ''
                log = f"{url_to_parse}: is not valid. Make a try by providing 'True' to 'Bypass Bozo' parameter"
                logger.info(log)

        return data
