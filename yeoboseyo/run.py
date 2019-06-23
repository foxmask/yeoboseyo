# coding: utf-8
"""
   여보세요 Run
"""
# std lib
from __future__ import unicode_literals
import datetime
import time
import asyncio
# external lib
import asks
import arrow
# starlette
from starlette.config import Config
# yeoboseyo
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
from yeoboseyo import JoplinService
from yeoboseyo import MastodonService
from yeoboseyo import RssService

config = Config('.env')


async def _update_date(trigger_id):
    """
    update the database table  with the execution date
    :param trigger_id: id to update
    :return: nothing
    """
    now = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
    trigger = await Trigger.objects.get(id=trigger_id)
    await trigger.update(date_triggered=now)


def get_published(entry):
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
    triggers = await Trigger.objects.all()
    for trigger in triggers:
        if trigger.status:
            print("Trigger {}".format(trigger.description))
            # RSS PART
            rss = RssService()
            # retrieve the data
            feeds = await rss.get_data(**{'url_to_parse': trigger.rss_url, 'bypass_bozo': config('BYPASS_BOZO')})
            now = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssZZ')
            date_triggered = arrow.get(trigger.date_triggered).format('YYYY-MM-DDTHH:mm:ssZZ')
            read_entries = 0
            created_entries = 0
            for entry in feeds.entries:
                # entry.*_parsed may be None when the date in a RSS Feed is invalid
                # so will have the "now" date as default
                published = get_published(entry)
                if published:
                    published = arrow.get(published).format('YYYY-MM-DDTHH:mm:ssZZ')
                # last triggered execution
                if date_triggered is not None and published is not None and now >= published >= date_triggered:
                    read_entries += 1
                    # JOPLIN PART
                    if trigger.joplin_folder:
                        res = await asks.get('{}:{}/ping'.format(config('JOPLIN_URL'), config('JOPLIN_PORT')))
                        if res.text == 'JoplinClipperServer':
                            joplin = JoplinService()
                            res = await joplin.save_data(trigger, entry)
                            if res:
                                created_entries += 1
                                await _update_date(trigger.id)
                            else:
                                print("Note not created in joplin, Something went wrong ")
                    # MASTODON PART
                    if trigger.mastodon:
                        masto = MastodonService()
                        res = await masto.save_data(trigger, entry)
                        if res:
                            created_entries += 1
                            await _update_date(trigger.id)
                        else:
                            print("Toot not created, Something went wrong ")
            if read_entries:
                print(" Entries created {} / Read {}".format(created_entries, read_entries))
            else:
                print("no feeds read")
    else:
        print('Check "Tools > Webclipper options"  if the service is enable')


# Bootstrap
if __name__ == '__main__':
    print('여보세요 ! RUN and GO')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
    loop.close()
