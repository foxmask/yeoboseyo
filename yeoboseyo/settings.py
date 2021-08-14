# coding: utf-8
"""
   여보세요 - Settings
"""

import logging
from starlette.config import Config
import databases
from starlette.datastructures import Secret

config = Config(".env")

###################################################
# Do not change anything below
# change the content of the `.env` file instead
# see env.sample for example values
###################################################

LOG_LEVEL = logging.INFO

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)

DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)

# server host and port
YEOBOSEYO_HOST = config('YEOBOSEYO_HOST', default='127.0.0.1')
YEOBOSEYO_PORT = config('YEOBOSEYO_PORT', cast=int, default=8000)
# time
TIME_ZONE = config('TIME_ZONE')
# format conversion
FORMAT_FROM = config('FORMAT_FROM', default='markdown_github')
FORMAT_TO = config('FORMAT_TO', default='html')
# For not well formed RSS
BYPASS_BOZO = config('BYPASS_BOZO', cast=bool, default=False)
# MASTODON
MASTODON_USERNAME = config('MASTODON_USERNAME')
MASTODON_PASSWORD = config('MASTODON_PASSWORD', cast=Secret)
MASTODON_INSTANCE = config('MASTODON_INSTANCE')
MASTODON_VISIBILITY = config('MASTODON_VISIBILITY')
# LOCAL STORAGE
MY_NOTES_FOLDER = config('MY_NOTES_FOLDER')
TEMPLATE_STYLE = config('TEMPLATE_STYLE')
# TELEGRAM
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN', cast=Secret)
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='', cast=Secret)
# SERVICE TOKEN
TOKEN = config('TOKEN', default='', cast=Secret)
# WALLABAG
WALLABAG_URL = config('WALLABAG_URL', default='')
WALLABAG_CLIENTID = config('WALLABAG_CLIENTID', default='', cast=Secret)
WALLABAG_CLIENTSECRET = config('WALLABAG_CLIENTSECRET', default='', cast=Secret)
WALLABAG_USERNAME = config('WALLABAG_USERNAME', default='', cast=Secret)
WALLABAG_PASSWORD = config('WALLABAG_PASSWORD', default='', cast=Secret)
