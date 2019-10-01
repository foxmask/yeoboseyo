# coding: utf-8
import argparse
import asyncio
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger

"""
this script allow to enable/disable a given trigger
"""


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
    print('여보세요 ! Switch')
    parser = argparse.ArgumentParser(description='Switch status of one trigger')
    parser.add_argument('trigger_id',
                        metavar='N',
                        type=int,
                        help='provide the id of the trigger to switch on/off')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(switch(args.trigger_id))
    loop.close()
