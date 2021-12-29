# coding: utf-8
"""
   여보세요 - Tests
"""

import databases
from starlette.datastructures import Secret
from yeoboseyo import settings


def test_config():
    """
    testing settings of the app
    :return:
    """
    assert hasattr(settings, 'DEBUG')
    assert hasattr(settings, 'DATABASE_URL')
    assert hasattr(settings, 'YEOBOSEYO_HOST')
    assert hasattr(settings, 'YEOBOSEYO_PORT')
    assert hasattr(settings, 'TIME_ZONE')
    assert hasattr(settings, 'FORMAT_FROM')
    assert hasattr(settings, 'FORMAT_TO')
    assert hasattr(settings, 'BYPASS_BOZO')
    assert hasattr(settings, 'MASTODON_USERNAME')
    assert hasattr(settings, 'MASTODON_PASSWORD')
    assert hasattr(settings, 'MASTODON_INSTANCE')
    assert hasattr(settings, 'MASTODON_VISIBILITY')
    assert hasattr(settings, 'MY_NOTES_FOLDER')
    assert hasattr(settings, 'TEMPLATE_STYLE')
    assert hasattr(settings, 'TELEGRAM_TOKEN')
    assert hasattr(settings, 'TELEGRAM_CHAT_ID')
    assert hasattr(settings, 'TOKEN')
    assert hasattr(settings, 'WALLABAG_URL')
    assert hasattr(settings, 'WALLABAG_USERNAME')
    assert hasattr(settings, 'WALLABAG_PASSWORD')
    assert hasattr(settings, 'WALLABAG_CLIENTID')
    assert hasattr(settings, 'WALLABAG_CLIENTSECRET')

    assert type(settings.DEBUG) is bool
    assert type(settings.DATABASE_URL) is databases.DatabaseURL
    assert type(settings.YEOBOSEYO_HOST) is str
    assert type(settings.YEOBOSEYO_PORT) is int
    assert type(settings.TIME_ZONE) is str
    assert type(settings.FORMAT_FROM) is str
    assert type(settings.FORMAT_TO) is str
    assert type(settings.BYPASS_BOZO) is bool
    assert type(settings.MASTODON_USERNAME) is str
    assert type(settings.MASTODON_PASSWORD) is Secret
    assert type(settings.MASTODON_INSTANCE) is str
    assert type(settings.MY_NOTES_FOLDER) is str
    assert type(settings.TELEGRAM_TOKEN) is Secret
    assert type(settings.TELEGRAM_CHAT_ID) is Secret
    assert type(settings.TOKEN) is Secret
    assert type(settings.WALLABAG_URL) is str
    assert type(settings.WALLABAG_USERNAME) is Secret
    assert type(settings.WALLABAG_PASSWORD) is Secret
    assert type(settings.WALLABAG_CLIENTID) is Secret
    assert type(settings.WALLABAG_CLIENTSECRET) is Secret
