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
    print("{:5} {:30} {:30} {:7} {:7} {:22}".format("ID", "Name", "Notebook", "Mastodon", "Status", "Triggered",))
    for trigger in triggers:
        date_triggered = trigger.date_triggered if trigger.date_triggered is not None else '***Not triggered yet**'
        joplin_folder = trigger.joplin_folder if trigger.joplin_folder is not None else '***Not used ***'
        print("{:5} {:<30} {:<30} {:>8} {:>7} {}".format(trigger.id,
                                                         trigger.description,
                                                         joplin_folder,
                                                         trigger.mastodon,
                                                         trigger.status,
                                                         date_triggered
                                                         )
              )

if __name__ == '__main__':
    print('여보세요 ! Report')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(report())
    loop.close()
