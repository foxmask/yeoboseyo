# coding: utf-8
import argparse
import arrow
import asyncio
import datetime
import os
from rich.console import Console
from rich.table import Table

import sys
from starlette.config import Config
import time

console = Console()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
from yeoboseyo import Rss

config = Config('.env')


async def report():
    triggers = await Trigger.objects.all()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Md Folder")
    table.add_column("Joplin Folder")
    table.add_column("Mastodon")
    table.add_column("Mail")
    table.add_column("Status")
    table.add_column("Triggered", style="dim")

    for trigger in triggers:
        status = "[green]Ok[/]" if trigger.status else "[yellow]Disabled[/]"
        masto = "[green]Ok[/]" if trigger.mastodon else "[yellow]Disabled[/]"
        mail = "[green]Ok[/]" if trigger.mail else "[yellow]Disabled[/]"
        date_triggered = trigger.date_triggered if trigger.date_triggered is not None else '***Not triggered yet**'
        joplin_folder = trigger.joplin_folder if trigger.joplin_folder is not None else '***Not used ***'
        localstorage = trigger.localstorage if trigger.localstorage is not None else '***Not used ***'
        table.add_row(str(trigger.id),
                      trigger.description,
                      localstorage,
                      joplin_folder,
                      masto,
                      mail,
                      status,
                      str(date_triggered))
    console.print(table)


async def switch(trigger_id):
    """

    :param trigger_id:  the id of the trigger to switch on/off
    :return:
    """
    trigger = await Trigger.objects.get(id=trigger_id)
    date_triggered = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
    await trigger.update(status=not trigger.status, date_triggered=date_triggered)
    msg = f"Successfully enabled Trigger '{trigger.description}'"
    if trigger.status is False:
        msg = f"Successfully disabled Trigger '{trigger.description}'"

    console.print(msg)


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


async def service(the_service, trigger, entry) -> int:
    """
    dynamic loading of service and submitting data to this one
    :param the_service:
    :param trigger:
    :param entry:
    :return:
    """
    # load the module/class + create class instance of the service
    klass = getattr(__import__('services.' + the_service.lower(), fromlist=[the_service]), the_service)
    # save the data
    if await klass().save_data(trigger, entry):
        return 1
    else:
        console.print(f'no {the_service} created')
        return 0


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
            # RSS PART
            rss = Rss()
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

                    if trigger.joplin_folder:
                        created_entries += await service('Joplin', trigger, entry)
                    if trigger.mail:
                        created_entries += await service('Mail', trigger, entry)
                    if trigger.mastodon:
                        created_entries += await service('Mastodon', trigger, entry)
                    if trigger.reddit:
                        created_entries += await service('Reddit', trigger, entry)
                    if trigger.localstorage:
                        created_entries += await service('LocalStorage', trigger, entry)

                    if created_entries > 0:
                        await _update_date(trigger.id)
                        console.print(f'[magenta]Trigger {trigger.description}[/] : '
                                      f'[green]{entry.title}[/]')

            if read_entries:
                console.print(f'[magenta]Trigger {trigger.description}[/] : '
                              f'[green]Entries[/] [bold]created[/] {created_entries} / '
                              f'[bold]Read[/] {read_entries}')
            else:
                console.print(f'[magenta]Trigger {trigger.description}[/] : no feeds read')


if __name__ == '__main__':
    console.print('[green]여보세요 ![/]')
    parser = argparse.ArgumentParser(prog="python run.py", description='Yeoboseyo')
    parser.add_argument('-a',
                        action='store',
                        choices=['report', 'go', 'switch'],
                        required=True,
                        help="choose -a report or -a go or -a switch -trigger_id <id>")
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
        asyncio.run(go())
    elif args.a == 'report':
        console.print(' [magenta]Report[/]')
        asyncio.run(report())
    elif args.a == 'switch':
        console.print(' [magenta]Switch[/]')
        if 'trigger_id' not in args or args.trigger_id == 0:
            console.print("You need to provide the ID you want to change.", style="red")
        else:
            asyncio.run(switch(args.trigger_id))
