# coding: utf-8
# std lib
from __future__ import unicode_literals
from logging import getLogger
# external lib
import asks
import feedparser
# create logger
logger = getLogger('yeoboseyo.yeoboseyo')

__all__ = ['RssService']


class RssService:

    async def get_data(self, **kwargs):
        """
        read the data from a given URL or path to a local file
        :param kwargs:
        :return: Feeds if Feeds well formed
        """
        if 'url_to_parse' not in kwargs:
            raise ValueError('you have to provide "url_to_parse" value')
        url_to_parse = kwargs['url_to_parse']
        bypass_bozo = kwargs.get('bypass_bozo', "False")
        data = await asks.get(url_to_parse)
        data = feedparser.parse(data.text)
        # if the feeds is not well formed, return no data at all
        if bypass_bozo is False and data.bozo == 1:
            data.entries = ''
            log = f"{url_to_parse}: is not valid. You can tick the checkbox "
            "'Bypass Feeds error ?' to force the process"
            logger.info(log)

        return data
