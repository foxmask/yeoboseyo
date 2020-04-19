# coding: utf-8
import argparse

import asyncio
import os
import sys

import arrow
from starlette.config import Config

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
from yeoboseyo.go import go
config = Config('.env')


async def report():
    triggers = await Trigger.objects.all()
    print("{:5} {:30} {:30} {:7} {:8} {:22}".format("ID", "Name", "Notebook", "Mastodon", "Status", "Triggered",))
    for trigger in triggers:
        status = "enabled" if trigger.status else "disabled"
        masto = "Yes" if trigger.mastodon else "No"
        date_triggered = trigger.date_triggered if trigger.date_triggered is not None else '***Not triggered yet**'
        joplin_folder = trigger.joplin_folder if trigger.joplin_folder is not None else '***Not used ***'
        print("{:5} {:<30} {:<30} {:>8} {:>8} {}".format(trigger.id,
                                                         trigger.description,
                                                         joplin_folder,
                                                         masto,
                                                         status,
                                                         date_triggered
                                                         )
              )


async def switch(trigger_id):
    """

    :param trigger_id:  the id of the trigger to switch on/off
    :return:
    """
    trigger = await Trigger.objects.get(id=trigger_id)
    date_triggered = trigger.date_triggered
    msg = f"Successfully enabled Trigger '{trigger.description}'"
    if trigger.status is False:
        msg = f"Successfully disabled Trigger '{trigger.description}'"
        date_triggered = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
    await trigger.update(status=not trigger.status, date_triggered=date_triggered)

    print(msg)


if __name__ == '__main__':
    print('여보세요 !', end="")
    parser = argparse.ArgumentParser(prog="python run.py", description='Yeoboseyo')
    parser.add_argument('-a',
                        action='store',
                        choices=['report', 'go', 'switch'],
                        required=True,
                        help="choose -a report or -a go or -a swtch -trigger_id <id>")
    parser.add_argument('-trigger_id',
                        action="store",
                        help="trigger id to switch of status",
                        type=int,
                        required=False,
                        default=0)
    args = parser.parse_args()
    if 'a' not in args:
        parser.print_help()
    elif args.a == 'go':
        """
        loop = asyncio.get_event_loop()
        try:
            print(' RUN and GO')
            loop.run_until_complete(go())
        finally:
            loop.close()
        """
        asyncio.run(go())
    elif args.a == 'report':
        print(' Report')
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(report())
        finally:
            loop.close()
        """
        asyncio.run(report())
    elif args.a == 'switch':
        print(' Switch')
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(switch(args.trigger_id))
        finally:
            loop.close()
        """
        asyncio.run(switch(args.trigger_id))
