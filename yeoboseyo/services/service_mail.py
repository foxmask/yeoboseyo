# coding: utf-8
# std lib
from __future__ import unicode_literals
# Import the email modules we'll need
from email.message import EmailMessage
from logging import getLogger
import smtplib
# yeoboseyo
from yeoboseyo.services import set_content
# starlette
from starlette.config import Config

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['MailService']


class MailService:

    format_to = 'html'
    format_from = 'markdown_github'
    email_server = 'localhost'
    email_sender = 'root'
    email_receiver = ''

    def __init__(self):
        """
        init parms
        """
        self.server = config('EMAIL_SERVER', default='localhost')
        self.sender = config('EMAIL_SENDER', default='root')
        self.receiver = config('EMAIL_RECEIVER')

    async def save_data(self, trigger, entry):
        """
        Send a new mail
        :param entry:
        :param trigger:
        :return: boolean
        """

        if trigger.mail:
            logger.debug(entry.title)
            logger.debug("%s %s %s" % (self.server, self.sender, self.receiver))

            msg = EmailMessage()
            msg.set_content(set_content(entry))

            msg['Subject'] = entry.title
            msg['From'] = self.sender
            msg['To'] = self.receiver

            with smtplib.SMTP(self.server) as s:
                s.send_message(msg)

        return True
