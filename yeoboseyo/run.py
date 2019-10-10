# coding: utf-8
import argparse

import asyncio
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
from yeoboseyo.go import go


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


async def switch(trigger_id):
    """

    :param trigger_id:  the id of the trigger to switch on/off
    :return:
    """
    trigger = await Trigger.objects.get(id=trigger_id)
    status = not trigger.status
    await trigger.update(status=status)
    print(f"Successfully switched Trigger '{trigger.description}' to {status}")


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
        loop = asyncio.get_event_loop()
        try:
            print(' RUN and GO')
            loop.run_until_complete(go())
        finally:
            loop.close()
    elif args.a == 'report':
        print(' Report')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(report())
        finally:
            loop.close()
    elif args.a == 'switch':
        print(' Switch')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(switch(args.trigger_id))
        finally:
            loop.close()
