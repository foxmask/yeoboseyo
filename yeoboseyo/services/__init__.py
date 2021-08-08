# coding: utf-8
"""
   여보세요 Service
"""
# std lib
from logging import getLogger
# external lib
import feedparser
import pypandoc
from starlette.config import Config

config = Config('.env')

# create logger
logger = getLogger(__name__)

__all__ = ['Service']


class Service:

    format_from = 'markdown_github'
    format_to = 'html'
    token = ''

    def __init__(self):
        """
        init parms
        """
        self.format_to = config('FORMAT_TO', default='html')
        self.format_from = config('FORMAT_FROM', default='markdown_github')
        self.token = config('TOKEN', default='')

    def _get_content(self, data, which_content):
        """
        check which content is present in the Feeds to return the right one
        :param data: feeds content
        :param which_content: one of content/summary_detail/description
        :return:
        """
        content = ''

        if data.get(which_content):
            if isinstance(data.get(which_content), feedparser.FeedParserDict):
                content = data.get(which_content)['value']
            elif not isinstance(data.get(which_content), str):
                if 'value' in data.get(which_content)[0]:
                    content = data.get(which_content)[0].value
            else:
                content = data.get(which_content)

        return content

    def set_content(self, entry):
        """
        which content to return ?
        :param entry:
        :return: the body of the RSS data
        """
        content = self._get_content(entry, 'content')

        if content == '':
            content = self._get_content(entry, 'summary_detail')

        if content == '':
            if entry.get('description'):
                content = entry.get('description')

        return content

    async def create_body_content(self, name, entry):
        """
        convert the HTML "body" into Markdown
        :param entry:
        :param name:
        :return:
        """
        # call pypandoc to convert html to markdown
        logger.debug("%s %s %s" % (self.set_content(entry), self.format_to, self.format_from))
        content = pypandoc.convert(self.set_content(entry), self.format_to, format=self.format_from)
        content += await self.footer(name, entry.link)
        return content

    async def footer(self, name, link):
        """

        :param name: name of the link
        :param link: link to lead the click to ;)
        :return:
        """
        if self.format_to == 'github_markdown':
            return '\n[Provided by {}]({})'.format(name, link)
        else:
            return '\n<a href="{}">Provided by {}</a>'.format(link, name)
