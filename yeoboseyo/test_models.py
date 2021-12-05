# coding: utf-8
"""
   여보세요 - Tests
"""
import databases
import orm
import os
import sys

import pytest

pytest_plugins = ('pytest_asyncio',)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from yeoboseyo.models import Trigger
database = databases.Database("sqlite:///db_test.sqlite")
models = orm.ModelRegistry(database=database)


@pytest.mark.asyncio
async def test_create():
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
