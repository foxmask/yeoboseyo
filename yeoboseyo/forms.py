# coding: utf-8
"""
   여보세요 Form SchemaValidation
"""
import typesystem


class TriggerSchema(typesystem.Schema):
    """
       Schema to define the structure of a Trigger
    """
    description = typesystem.String(title="Description", max_length=200)
    rss_url = typesystem.String(title="RSS URL", max_length=255)
    localstorage = typesystem.String(title="Markdown Folder", allow_blank=True)
    tags = typesystem.String(title="Tags", max_length=255)
    status = typesystem.Boolean(title="Status", default=False)
