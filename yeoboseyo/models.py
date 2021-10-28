# coding: utf-8
"""
   여보세요 - Models
"""

import databases
import datetime
import orm
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)
from yeoboseyo import settings

database = databases.Database(settings.DATABASE_URL, force_rollback=True)
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


# Bootstrap
if __name__ == '__main__':
    # Create the database
    print(f"database creation {settings.DATABASE_URL}")
    # Create the tables
    models.create_all()
    print("done!")
