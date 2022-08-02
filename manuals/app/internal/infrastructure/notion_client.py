import os
from typing import List

import environ
from django.conf import settings
from notion_client import Client


class NotionClient:
    def __init__(self):
        BASE_DIR = settings.BASE_DIR
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
        self.notion_client = Client(auth=env("INTEGRATION_TOKEN"))

    def page(self, id):
        return self.notion_client.blocks.retrieve(id)

    def page_children(self, id):
        return self.notion_client.blocks.children.list(id)

    def db(self, id):
        return self.notion_client.databases.retrieve(id)

    def db_children(self, id):
        return self.notion_client.databases.query(id)
    
    def page_children_from_cursor(self, id, cursor_id) -> List:
        return self.notion_client.blocks.children.list(id, start_cursor=cursor_id)
