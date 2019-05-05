# coding: utf-8
import asyncio
from yeoboseyo.models import Trigger

"""
this script will display a list of all the details of the triggers
"""


async def report():
    triggers = await Trigger.objects.all()
    print("{:<5} {:<30} {:<22} {:<30} {:<6}".format("ID", "Name", "Triggered", "Notebook", "Status"))
    for trigger in triggers:
        fill = '      '
        print("{:5} {:<30} {:%Y-%m-%d %H:%M}{} {:<30} {:<6}".format(trigger.id,
                                                                    trigger.description,
                                                                    trigger.date_triggered,
                                                                    fill,
                                                                    trigger.joplin_folder,
                                                                    trigger.status))

if __name__ == '__main__':
    print('여보세요 ! Report')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(report())
    loop.close()
