# coding: utf-8
"""
   여보세요 - Form SchemaValidation
"""

import typesystem

"""
   Schema to define the structure of a Trigger
"""
trigger_schema = typesystem.Schema(
    fields={
        "description": typesystem.String(title="Description", max_length=200),
        "rss_url": typesystem.String(title="RSS URL", max_length=255),
        "localstorage": typesystem.String(title="Create files in that Markdown folder", allow_blank=True),
        "webhook": typesystem.String(title="Publish on slack/mattermost/discord?", max_length=255, allow_blank=True),
        "mastodon": typesystem.Boolean(title="Publish on Mastodon?", default=True),
        "telegram": typesystem.Boolean(title="Publish on Telegram?", default=True),
        "wallabag": typesystem.Boolean(title="Add articles on Wallabag?", default=False),
        "status": typesystem.Boolean(title="Status", default=True)
    }
)
