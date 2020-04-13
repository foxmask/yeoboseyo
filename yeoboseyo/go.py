# coding: utf-8
"""
   여보세요 Go
"""
# std lib
from __future__ import unicode_literals
import datetime
from logging import getLogger
import logging.config
import os
import sys
import time
# external lib
import arrow
from starlette.config import Config
# yeoboseyo

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
from yeoboseyo import JoplinService, RssService

config = Config('.env')

# create logger
logging.config.fileConfig('logging.conf')
logger = getLogger(__name__)


async def _update_date(trigger_id) -> None:
    """
    update the database table  with the execution date
    :param trigger_id: id to update
    :return: nothing
    """
    now = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
    trigger = await Trigger.objects.get(id=trigger_id)
    await trigger.update(date_triggered=now)


def get_published(entry) -> datetime:
    """
    get the 'published' attribute
    :param entry:
    :return: datetime
    """
    published = None
    if hasattr(entry, 'published_parsed'):
        if entry.published_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.published_parsed))
    elif hasattr(entry, 'created_parsed'):
        if entry.created_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.created_parsed))
    elif hasattr(entry, 'updated_parsed'):
        if entry.updated_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.updated_parsed))
    return published


async def service(the_service, trigger, entry, created_entries) -> int:
    """
    dynamic loading of service and submitting data to this one
    :param the_service:
    :param trigger:
    :param entry:
    :param created_entries:
    :return:
    """
    service_name = the_service.split('Service')[0]  # name of the service
    # load the module/class + create class instance of the service
    klass = getattr(__import__('services.service_' + service_name.lower(), fromlist=[the_service]), the_service)
    # save the data
    if await klass().save_data(trigger, entry):
        created_entries += 1
    else:
        logger.info("no %s created" % service_name)
    return created_entries


async def go():
    """
    this function:
    - check if joplinwebclipper is available
    - get the triggers where the status is On
    - get the RSS Feed of that trigger
    - compare the date of the feed item with the last triggered date of that trigger
    - if item date > triggered date ; create a Joplin Note in the choosen folder
    - then reports how many data have been created
    :return:
    """
    if await JoplinService().check_service() is False:
        raise ConnectionError("Joplin service is not started")
    triggers = await Trigger.objects.all()
    for trigger in triggers:
        if trigger.status:
            logger.info("Trigger {}".format(trigger.description))
            # RSS PART
            rss = RssService()
            # retrieve the data
            feeds = await rss.get_data(**{'url_to_parse': trigger.rss_url, 'bypass_bozo': config('BYPASS_BOZO')})
            now = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DDTHH:mm:ssZZ')
            date_triggered = arrow.get(trigger.date_triggered).format('YYYY-MM-DDTHH:mm:ssZZ')

            read_entries = 0
            created_entries = 0
            for entry in feeds.entries:
                # entry.*_parsed may be None when the date in a RSS Feed is invalid
                # so will have the "now" date as default
                published = get_published(entry)
                if published:
                    published = arrow.get(published).to(config('TIME_ZONE')).format('YYYY-MM-DDTHH:mm:ssZZ')
                # last triggered execution
                if published is not None and now >= published >= date_triggered:
                    read_entries += 1

                    created_entries = await service('JoplinService', trigger, entry, created_entries)
                    created_entries = await service('MailService', trigger, entry, created_entries)
                    created_entries = await service('MastodonService', trigger, entry, created_entries)
                    created_entries = await service('RedditService', trigger, entry, created_entries)

                    if created_entries > 0:
                        await _update_date(trigger.id)
                        logger.info("%s %s" % (trigger, entry.title))

            if read_entries:
                logger.info(f'Entries created {created_entries} / Read {read_entries}')
            else:
                logger.info("no feeds read")
