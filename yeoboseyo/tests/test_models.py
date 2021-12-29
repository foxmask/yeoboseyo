# coding: utf-8
"""
   여보세요 - Tests
"""
import databases
import datetime
import pytest
import orm
import os

pytestmark = pytest.mark.anyio

assert "TEST_DATABASE_URL" in os.environ, "TEST_DATABASE_URL is not set."
DATABASE_URL = os.environ["TEST_DATABASE_URL"]

database = databases.Database(DATABASE_URL)
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


@pytest.fixture(autouse=True, scope="function")
async def create_test_database():
    await models.create_all()
    yield
    await models.drop_all()


async def test_create():
    trigger = await Trigger.objects.create(
        description="My Blog",
        rss_url="https://foxmask.org/feeds/atom.rss",
        mastodon=False,
        telegram=False,
        wallabag=False,
        webhook="",
        localstorage="/home/foxmask/Notes/",
        status=True
    )
    assert trigger.description == 'My Blog'
    assert type(trigger.rss_url) is str
    assert type(trigger.localstorage) is str
    assert type(trigger.mastodon) is bool
    assert type(trigger.telegram) is bool
    assert type(trigger.wallabag) is bool
    assert trigger.webhook is None
    assert type(trigger.status) is bool
    return trigger


async def test_get():
    trigger = await test_create()
    assert trigger.rss_url == "https://foxmask.org/feeds/atom.rss"
