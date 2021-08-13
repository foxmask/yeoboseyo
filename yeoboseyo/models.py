# coding: utf-8
"""
   여보세요 Models
"""
import databases
import datetime
import orm
import sqlalchemy
from yeoboseyo import settings

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.DATABASE_URL, force_rollback=True)


class Trigger(orm.Model):
    __tablename__ = "trigger"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    rss_url = orm.String(max_length=255)
    mastodon = orm.Boolean(default=False)
    telegram = orm.Boolean(default=False)
    webhook = orm.String(max_length=255)
    wallabag = orm.Boolean(default=False)
    localstorage = orm.String(max_length=255, allow_null=True)
    description = orm.String(max_length=200)
    date_created = orm.DateTime(default=datetime.datetime.now)
    date_triggered = orm.DateTime(default=datetime.datetime.now)
    status = orm.Boolean(default=False)


# Bootstrap
if __name__ == '__main__':
    # Create the database
    print(f"database creation {settings.DATABASE_URL}")
    engine = sqlalchemy.create_engine(settings.DATABASE_URL)
    metadata.create_all(engine)
    print("done!")
