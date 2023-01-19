import os
import time
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
        self.retries_count = 3
        self.delay_seconds = 3


    def page(self, id):
        for i in range(self.retries_count):
            try:
                return self.notion_client.blocks.retrieve(id)
            except Exception as e:
                print(e)
                time.sleep(self.delay_seconds)

    def page_children(self, id):
        for i in range(self.retries_count):
            try:
                return self.notion_client.blocks.children.list(id)
            except Exception as e:
                print(e)
                time.sleep(self.delay_seconds)
        return 

    def db(self, id):
        for i in range(self.retries_count):
            try:
                return self.notion_client.databases.retrieve(id)
            except Exception as e:
                print(e)
                time.sleep(self.delay_seconds)

    def db_children(self, id):
        for i in range(self.retries_count):
            try:
                return self.notion_client.databases.query(id)
            except Exception as e:
                print(e)
                time.sleep(self.delay_seconds)
    
    def page_children_from_cursor(self, id, cursor_id) -> List:
        for i in range(self.retries_count):
            try:
                return self.notion_client.blocks.children.list(id, start_cursor=cursor_id)
            except Exception as e:
                print(e)
                time.sleep(self.delay_seconds)
