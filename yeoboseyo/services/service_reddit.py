# coding: utf-8
# std lib
from __future__ import unicode_literals
from logging import getLogger
# external lib
from praw import Reddit
# starlette
from starlette.config import Config

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['RedditService']


class RedditService:
    """
        Service Mastodon
    """
    def __init__(self):
        self.reddit = Reddit(client_id=config('REDDIT_CLIENT_ID'), client_secret=config('REDDIT_CLIENT_SECRET'),
                             password=config('REDDIT_PASSWORD'), user_agent=config('REDDIT_USERAGENT'),
                             username=config('REDDIT_USERNAME'))

    async def save_data(self, trigger, entry):
        """
        Post a new toot to Mastodon
        :param entry:
        :param trigger:
        :return: boolean
        """
        status = False
        try:
            self.reddit.subreddit(trigger.subreddit).submit(entry.title, url=entry.link)
            status = True
        except ValueError as e:
            logger.error(e)
            status = False

        return status
