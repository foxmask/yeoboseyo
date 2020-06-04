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

    joplin_folder = typesystem.String(title="Joplin Folder", max_length=80, allow_blank=True)
    reddit = typesystem.String(title="Subreddit", max_length=80, allow_blank=True)
    localstorage = typesystem.String(title="Markdown Folder", allow_blank=True)

    mail = typesystem.Boolean(title="Send a mail ?", default=False)
    mastodon = typesystem.Boolean(title="Publish on Mastodon ?", default=False)
    status = typesystem.Boolean(title="Status", default=False)
