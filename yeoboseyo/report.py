# coding: utf-8
import asyncio
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)
from yeoboseyo.models import Trigger

"""
this script will display a list of all the details of the triggers
"""


async def report():
    triggers = await Trigger.objects.all()
    print("{:<5} {:<30} {:<22} {:<30} {:<6} {:<6}".format("ID", "Name", "Triggered", "Notebook", "Mastodon", "Status"))
    for trigger in triggers:
        fill = ''
        date_triggered = trigger.date_triggered if trigger.date_triggered is not None else ''
        print("{:5} {:<30} {:<22}{:<6} {:<30} {:<6} {:<6}".format(trigger.id,
                                                                  trigger.description,
                                                                  date_triggered,
                                                                  fill,
                                                                  trigger.joplin_folder,
                                                                  trigger.mastodon,
                                                                  trigger.status))

if __name__ == '__main__':
    print('여보세요 ! Report')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(report())
    loop.close()
