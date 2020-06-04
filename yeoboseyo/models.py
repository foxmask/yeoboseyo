# coding: utf-8
"""
   여보세요 Models
"""
import databases
import datetime
import orm
from starlette.config import Config
import sqlalchemy

metadata = sqlalchemy.MetaData()
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')
database = databases.Database(DATABASE_URL, force_rollback=True)


class Trigger(orm.Model):
    __tablename__ = "trigger"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    rss_url = orm.String(max_length=255)
    joplin_folder = orm.String(max_length=80, allow_null=True)
    reddit = orm.String(max_length=80, allow_null=True)
    mastodon = orm.Boolean(default=False)
    mail = orm.Boolean(default=False)
    localstorage = orm.String(max_length=255, allow_null=True)
    description = orm.String(max_length=200)
    date_created = orm.DateTime(default=datetime.datetime.now)
    date_triggered = orm.DateTime(default=datetime.datetime.now)
    status = orm.Boolean(default=False)


# Bootstrap
if __name__ == '__main__':
    # Create the database
    print(f"database creation {DATABASE_URL}")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    print("done!")
