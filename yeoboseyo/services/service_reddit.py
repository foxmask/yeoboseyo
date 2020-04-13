# coding: utf-8
"""
   여보세요 Service Reddit
"""
# std lib
from __future__ import unicode_literals
from logging import getLogger
# external lib
from praw import Reddit
from starlette.config import Config
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['RedditService']


class RedditService(Service):
    """
        Service Mastodon
    """
    def __init__(self):
        super(RedditService, self).__init__()
        self.reddit = Reddit(client_id=config('REDDIT_CLIENT_ID'), client_secret=config('REDDIT_CLIENT_SECRET'),
                             password=config('REDDIT_PASSWORD'), user_agent=config('REDDIT_USERAGENT'),
                             username=config('REDDIT_USERNAME'))

    async def save_data(self, trigger, entry) -> bool:
        """
        Post a new toot to Mastodon
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        status = False
        if trigger.reddit:
            try:
                self.reddit.subreddit(trigger.reddit).submit(entry.title, url=entry.link)
                status = True
            except ValueError as e:
                logger.error(e)
                status = False

        return status
