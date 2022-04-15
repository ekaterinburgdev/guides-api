import os

import environ
from django.conf import settings
from notion_client import Client

BASE_DIR = settings.BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
notion_client = Client(auth=env("INTEGRATION_TOKEN"))
