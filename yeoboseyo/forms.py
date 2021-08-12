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
    localstorage = typesystem.String(title="Create Files in that Markdown Folder", allow_blank=True)
    webhook = typesystem.String(title="Publish on slack/mattermost/discord?", max_length=255, allow_blank=True)
    mastodon = typesystem.Boolean(title="Publish on Mastodon?", default=True)
    telegram = typesystem.Boolean(title="Publish on Telegram?", default=True)
    status = typesystem.Boolean(title="Status", default=True)
