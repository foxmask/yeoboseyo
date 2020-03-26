# coding: utf-8
"""
   여보세요 Service Joplin
"""
# std lib
from __future__ import unicode_literals
from logging import getLogger
# external lib
import httpx
from starlette.config import Config
import sys
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['JoplinService']


class JoplinService(Service):

    joplin_port = 41184
    joplin_url = 'http://127.0.0.1'

    def __init__(self):
        """
        init parms
        """
        super(JoplinService, self).__init__()
        # overwritting config
        self.format_to = 'markdown_github'
        self.format_from = 'html'

        self.joplin_port = config('JOPLIN_PORT', default=41184)
        self.joplin_url = config('JOPLIN_URL', default='http://127.0.0.1')

    async def get_folders(self):
        """
        get the list of all the folders of the joplin profile
        :return:
        """
        async with httpx.AsyncClient() as client:
            res = await client.get("{}:{}/folders".format(self.joplin_url, self.joplin_port))
            return res.json()

    async def save_data(self, trigger, entry):
        """
        Post a new note to the JoplinWebclipperServer
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """
        if trigger.joplin_folder:
            # get the content of the Feeds
            content = await self.create_body_content(trigger.description, entry)
            # build the json data
            folders = await self.get_folders()

            notebook_id = 0
            for folder in folders:
                if folder.get('title') == trigger.joplin_folder:
                    notebook_id = folder.get('id')
            if notebook_id == 0:
                for folder in folders:
                    if 'children' in folder:
                        for child in folder.get('children'):
                            if child.get('title') == trigger.joplin_folder:
                                notebook_id = child.get('id')
            data = {'title': entry.title,
                    'body': content,
                    'parent_id': notebook_id,
                    'author': entry.author,
                    'source_url': entry.link}
            url = "{}:{}/notes".format(self.joplin_url, self.joplin_port)
            logger.debug(url)
            logger.debug(data)
            async with httpx.AsyncClient() as client:
                res = await client.post(url, json=data)
            if res.status_code == 200:
                return True
        return False

    async def check_service(self):
        url = '{}:{}/ping'.format(config('JOPLIN_URL'), config('JOPLIN_PORT'))
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(url)
                if res.text == 'JoplinClipperServer':
                    return True
            except OSError as e:
                print("Connection failed to {}. Check if joplin is started".format(url))
                print(e)
                print('Yeoboseyo aborted!')
                sys.exit(1)
