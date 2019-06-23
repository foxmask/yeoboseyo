# coding: utf-8
"""
   여보세요 Run
"""
# std lib
from __future__ import unicode_literals
# starlette
from starlette.config import Config

from logging import getLogger

from mastodon import Mastodon

# create logger
logger = getLogger('yeoboseyo.yeoboseyo')

config = Config('.env')
from pathlib import Path

my_file = Path("yeoboseyo_clientcred")
if my_file.is_file():
    print("credential already exists this script should be run only ONCE, if you really want to recrate it , drop it first")
else:
    # create app
    Mastodon.create_app(
        "Yeoboseyo",
        api_base_url=config('MASTODON_INSTANCE'),
        to_file='yeoboseyo_clientcred.secret')

    mastodon = Mastodon(
        client_id='yeoboseyo_clientcred.secret',
        api_base_url=config('MASTODON_INSTANCE')
    )
    mastodon.log_in(
        config('MASTODON_USERNAME'),
        config('MASTODON_PASSWORD'),
        to_file='yeoboseyo_clientcred.secret'
    )
