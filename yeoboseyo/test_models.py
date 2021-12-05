# coding: utf-8
"""
   여보세요 - Tests
"""
import databases
import datetime
import orm
import os
import sys

import pytest

pytest_plugins = ('pytest_asyncio',)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger

database = databases.Database("sqlite:///db_test.sqlite3")
models = orm.ModelRegistry(database=database)


class Trigger(orm.Model):
    tablename = "trigger"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "rss_url": orm.String(max_length=255),
        "mastodon": orm.Boolean(default=False),
        "telegram": orm.Boolean(default=False),
        "webhook": orm.String(max_length=255, allow_null=True),
        "wallabag": orm.Boolean(default=False),
        "localstorage": orm.String(max_length=255, allow_null=True),
        "description": orm.String(max_length=200),
        "date_created": orm.DateTime(default=datetime.datetime.now),
        "date_triggered": orm.DateTime(default=datetime.datetime.now),
        "status": orm.Boolean(default=False)
    }


@pytest.mark.asyncio
async def test_create():
    await models.create_all()
    return await Trigger.objects.create(
        rss_url="https://foxmask.org/feeds/atom.rss",
        mastodon=False,
        telegram=False,
        wallabag=False,
        webhook="",
        localstorage="/home/foxmask/Notes/",
        description="My Blog",
        status=True
    )


@pytest.mark.asyncio
async def test_get():
    trigger = await test_create()
    assert trigger.rss_url == "https://foxmask.org/feeds/atom.rss"
    print(trigger)
