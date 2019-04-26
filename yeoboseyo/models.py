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

    id  = orm.Integer(primary_key=True)
    rss_url = orm.String(max_length=255)
    joplin_folder = orm.String(max_length=80)
    description = orm.String(max_length=200)
    date_created = orm.DateTime(default=datetime.datetime.now)
    date_triggered = orm.DateTime(allow_null=True)
    status = orm.Boolean(default=False)
    result = orm.Text(allow_null=True)
    date_result = orm.DateTime(allow_null=True)
    provider_failed = orm.Integer(allow_null=True)
    consumer_failed = orm.Integer(allow_null=True)

# Bootstrap
if __name__ == '__main__':
    # Create the database
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)