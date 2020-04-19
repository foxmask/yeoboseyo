# coding: utf-8
"""
   여보세요 Service Mail
"""
# std lib
from __future__ import unicode_literals
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
import smtplib
# external lib
from starlette.config import Config
# yeoboseyo
from yeoboseyo.services import Service

# create logger
logger = getLogger(__name__)

config = Config('.env')

__all__ = ['Mail']


class Mail(Service):

    email_server = 'localhost'
    email_sender = 'root'
    email_receiver = ''

    def __init__(self):
        """
        init parms
        """
        super().__init__()
        self.email_server = config('EMAIL_SERVER', default='localhost')
        self.email_sender = config('EMAIL_SENDER', default='root')
        self.email_receiver = config('EMAIL_RECEIVER')

    async def save_data(self, trigger, entry) -> bool:
        """
        Send a new mail
        :param trigger: current trigger
        :param entry: data from Feeds
        :return: boolean
        """

        if trigger.mail:
            logger.debug("%s From: %s - To: %s - Title: %s" %
                         (self.email_server, self.email_sender, self.email_receiver, entry.title))

            body = await self.create_body_content(trigger.description, entry)

            msg = MIMEMultipart('alternative')

            part1 = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
            part2 = MIMEText(body.encode('utf-8'), 'html', 'utf-8')
            msg.attach(part1)
            msg.attach(part2)

            msg['Subject'] = entry.title
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver

            with smtplib.SMTP(self.email_server) as s:
                s.sendmail(self.email_sender, self.email_receiver, msg.as_string())
        return True
