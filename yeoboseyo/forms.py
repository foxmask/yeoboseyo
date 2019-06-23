# coding: utf-8
"""
   여보세요 Form SchemaValidation
"""
import typesystem


class TriggerSchema(typesystem.Schema):
    """
       Schema to define the structure of a Trigger
    """
    rss_url = typesystem.String(title="RSS URL", max_length=255)
    joplin_folder = typesystem.String(title="Joplin Folder", max_length=80)
    mastodon = typesystem.Boolean(title="Publish on Mastodon ?", default=False)
    description = typesystem.String(title="Description", max_length=200)
    # date_created = typesystem.DateTime(default=datetime.date.today)
    # date_triggered = typesystem.DateTime(allow_null=True)
    status = typesystem.Boolean(title="Status", default=False)
    # result = typesystem.Text(allow_null=True)
    # date_result = typesystem.DateTime(allow_null=True)
    # counter_ok = typesystem.Integer(allow_null=True)
    # counter_ko = typesystem.Integer(allow_null=True)

