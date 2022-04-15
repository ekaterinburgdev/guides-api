import os

from django.conf import settings

BASE_DIR = settings.BASE_DIR
STATIC_DIR = os.path.join(os.path.join(BASE_DIR, "app"), "static")
