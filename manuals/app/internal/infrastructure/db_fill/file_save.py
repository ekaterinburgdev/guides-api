import os
import urllib.request

from manuals.app.internal.infrastructure.db_fill.constants import STATIC_DIR
from .content_getters import save_any_format_image


def save_file(file):
    name = file["name"].replace(" ", "_")
    if name[-4:] == ".pdf":
        return save_pdf(file, name)
    return save_any_format_image(file["file"]["url"])

def save_pdf(file, name):
    image_location = os.path.join(STATIC_DIR, name)
    urllib.request.urlretrieve(file["file"]["url"], image_location)
    return name