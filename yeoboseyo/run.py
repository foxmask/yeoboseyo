# coding: utf-8
import argparse
import arrow
import asyncio
import os
import sys
from starlette.config import Config

from rich.console import Console
from rich.table import Table

console = Console()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
from yeoboseyo.go import go
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


if __name__ == '__main__':
    console.print('[green]여보세요 ![/]', end="")
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
