import logging
from starlette.config import Config
import databases
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)

DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)


YEOBOSEYO_HOST = config('YEOBOSEYO_HOST', default='127.0.0.1')
YEOBOSEYO_PORT = config('YEOBOSEYO_PORT', cast=int, default=8000)
TIME_ZONE = config('TIME_ZONE')
FORMAT_FROM = config('FORMAT_FROM', default='markdown_github')
FORMAT_TO = config('FORMAT_TO', default='html')
BYPASS_BOZO = config('BYPASS_BOZO', cast=bool, default=False)
LOG_LEVEL = logging.INFO
MASTODON_USERNAME = config('MASTODON_USERNAME')
MASTODON_PASSWORD = config('MASTODON_PASSWORD', cast=Secret)
MASTODON_INSTANCE = config('MASTODON_INSTANCE')
MASTODON_VISIBILITY = config('MASTODON_VISIBILITY')
MY_NOTES_FOLDER = config('MY_NOTES_FOLDER')
TEMPLATE_STYLE = config('TEMPLATE_STYLE')
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN', cast=Secret)
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='', cast=Secret)
TOKEN = config('TOKEN', default='', cast=Secret)
WALLABAG_URL = config('WALLABAG_URL', default='')
WALLABAG_CLIENTID = config('WALLABAG_CLIENTID', default='', cast=Secret)
WALLABAG_CLIENTSECRET = config('WALLABAG_CLIENTSECRET', default='', cast=Secret)
WALLABAG_USERNAME = config('WALLABAG_USERNAME', default='', cast=Secret)
WALLABAG_PASSWORD = config('WALLABAG_PASSWORD', default='', cast=Secret)
