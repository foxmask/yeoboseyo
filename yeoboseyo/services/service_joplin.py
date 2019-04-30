# coding: utf-8
# std lib
from __future__ import unicode_literals
from logging import getLogger
# external lib
import asks
import pypandoc
# starlette
from starlette.config import Config
# yeoboseyo
from yeoboseyo.services import set_content
# create logger
logger = getLogger('yeoboseyo.yeoboseyo')

config = Config('.env')

__all__ = ['JoplinService']


class JoplinService:

    format_to = 'html'
    format_from = 'markdown_github'
    joplin_port = 41184
    joplin_url = 'http://127.0.0.1'

    def __init__(self):
        """
        init parms
        """
        self.format_to = config('FORMAT_TO', default='html')
        self.format_from = config('FORMAT_FROM', default='markdown_github')
        self.joplin_port = config('JOPLIN_PORT', default=41184)
        self.joplin_url = config('JOPLIN_URL', default='http://127.0.0.1')

    async def create_note_content(self, name, entry):
        """
        convert the HTML "body" into Markdown
        :param entry:
        :param name:
        :return:
        """
        # call pypandoc to convert html to markdown
        content = pypandoc.convert(set_content(entry), self.format_from, format=self.format_to)
        content += '\n[Provided by {}]({})'.format(name, entry.link)
        return content

    async def get_folders(self):
        """
        get the list of all the folders of the joplin profile
        :return:
        """
        res = await asks.get("{}:{}/folders".format(self.joplin_url, self.joplin_port))
        return res.json()

    async def save_data(self, trigger, entry):
        """
        Post a new note to the JoplinWebclipperServer
        :param entry:
        :param trigger:
        :return: boolean
        """
        # get the content of the Feeds
        content = await self.create_note_content(trigger.description, entry)
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
        res = await asks.post(url, json=data)
        if res.status_code == 200:
            return True
        return False
