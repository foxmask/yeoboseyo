# coding: utf-8
"""
   여보세요 - Running Engine
"""

import argparse
import arrow
import asyncio
import datetime
from feedsparser_data import RssAsync as Rss
from rich.console import Console
from rich.table import Table
import time

import settings
from models import Trigger

console = Console()

now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DDTHH:mm:ssZZ')

######################################
#  methods that 'calculate' something
######################################


async def _update_date(trigger_id) -> None:
    """
    update the database table  with the execution date
    :param trigger_id: id to update
    :return: nothing
    """
    trigger = await Trigger.objects.get(id=trigger_id)
    await trigger.update(date_triggered=now)


def _get_published(entry) -> datetime:
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


async def _service(the_service, status, trigger, entry) -> int:
    """
    dynamic loading of service and submitting data to this one
    :param the_service:
    :status status: boolean : is the service on ?
    :param trigger:
    :param entry:
    :return:
    """
    if status:
        attr = the_service.lower()
        # check if the attributes mastodon, localstorage are set
        # to trigger the associated service
        class_to_import = 'yeoboseyo.services.' + the_service.lower()
        if getattr(trigger, attr):
            klass = getattr(__import__(class_to_import, fromlist=[the_service]), the_service)
            # save the data
            if await klass().save_data(trigger, entry):
                return 1
            else:
                console.print(f'no {the_service} created')
    else:
        console.print(f'{the_service} is {status}')
    return 0


################################################
#  methods that display something on the screen
################################################


async def switch(trigger_id):
    """

    :param trigger_id:  the id of the trigger to switch on/off
    :return:
    """
    trigger = await Trigger.objects.get(id=trigger_id)
    date_triggered = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')
    await trigger.update(status=not trigger.status, date_triggered=date_triggered)
    msg = f"Successfully enabled Trigger '{trigger.description}'"
    if trigger.status is False:
        msg = f"Successfully disabled Trigger '{trigger.description}'"

    console.print(msg)


async def report():
    triggers = await Trigger.objects.all()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Md Folder")
    table.add_column("Mastodon")
    table.add_column("Telegram")
    table.add_column("Webhook")
    table.add_column("Wallabag")
    table.add_column("Status")
    table.add_column("Triggered", style="dim")

    for trigger in triggers:
        status = "[green]Ok[/]" if trigger.status else "[yellow]Disabled[/]"
        masto = "[green]Ok[/]" if trigger.mastodon else "[yellow]Disabled[/]"
        telegram = "[green]Ok[/]" if trigger.telegram else "[yellow]Disabled[/]"
        webhook = "[green]Ok[/]" if trigger.webhook else "[yellow]Disabled[/]"
        wallabag = "[green]Ok[/]" if trigger.wallabag else "[yellow]Disabled[/]"
        date_triggered = trigger.date_triggered if trigger.date_triggered is not None else '***Not triggered yet**'
        localstorage = trigger.localstorage if trigger.localstorage is not None else '***Not used ***'
        table.add_row(str(trigger.id),
                      trigger.description,
                      localstorage,
                      masto,
                      telegram,
                      webhook,
                      wallabag,
                      status,
                      str(date_triggered))
    console.print(table)


async def go():
    """
    - get the triggers where the status is On
    - get the RSS Feed of that trigger
    - compare the date of the feed item with the last triggered date of that trigger
    - if item date > triggered date ; create a Joplin Note in the choosen folder
    - then reports how many data have been created
    :return:
    """
    triggers = await Trigger.objects.all(status=True)
    for trigger in triggers:

        rss = Rss()
        feeds = await rss.get_data(
            **{'url_to_parse': trigger.rss_url,
               'bypass_bozo': settings.BYPASS_BOZO}
        )
        date_triggered = arrow.get(trigger.date_triggered).format('YYYY-MM-DDTHH:mm:ssZZ')

        read_entries = 0
        created_entries = 0
        for entry in feeds.entries:
            # entry.*_parsed may be None when the date in a RSS Feed is invalid
            # so will have the "now" date as default
            published = _get_published(entry)
            if published:
                published = arrow.get(published).to(settings.TIME_ZONE).format('YYYY-MM-DDTHH:mm:ssZZ')
            # last triggered execution
            if published is not None and now >= published >= date_triggered:
                read_entries += 1

                for service in list(settings.SUPPORTED_SERVICES):
                    # hasattr(trigger, service.lower()) => retrieve trigger.mastodon / trigger.localstorage and so on
                    # attr = value of the trigger.<service>
                    attr = hasattr(trigger, service.lower())
                    created_entries += await _service(service,
                                                      status=attr,
                                                      trigger=trigger,
                                                      entry=entry)
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
