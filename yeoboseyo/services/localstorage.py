# coding: utf-8
"""
   여보세요 Service LocalStorage
"""
# std lib
from __future__ import unicode_literals
from logging import getLogger
from pathlib import Path
# external lib
from jinja2 import Environment, PackageLoader
from slugify import slugify
from starlette.config import Config
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['LocalStorage']


class LocalStorage(Service):

    local_storage = ""

    def __init__(self):

        super().__init__()
        self.format_to = "markdown_github"
        self.format_from = "html"
        self.local_storage = config('MY_NOTES_FOLDER')

    async def save_data(self, trigger, entry) -> bool:
        """
        Create a new note to the config('MY_NOTES_FOLDER')
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        # get the content of the Feeds
        content = await self.create_body_content(trigger.description, entry)
        p = Path(self.local_storage + '/' + trigger.localstorage)
        try:
            author = entry.author
        except AttributeError:
            author = '' # Not all feeds always provide an author
        if p.is_dir():
            data = {'title': entry.title,
                    'body': content,
                    'author': author,
                    'source_url': entry.link,
                    'localstorage': trigger.localstorage}
            logger.debug(data)
            yesno = await self.save_file(**data)
            return yesno
        return False

    async def save_file(self, **data):
        """

        :param data:
        :return: boolean
        """
        env = Environment(
            loader=PackageLoader('yeoboseyo', 'templates'),
        )
        template = env.get_template('localstorage.md')
        output = template.render(data=data)
        folder = data['localstorage']
        file_name = slugify(data['title']) + '.md'
        file_md = f'{self.local_storage}/{folder}/{file_name}'
        # overwrite existing file with same slug name
        with open(file_md, 'w') as ls:
            ls.write(output)
            result = True

        return result
