import os
import urllib.request

from .constants import STATIC_DIR
from .content_getters import save_any_format_image_as


def save_file(file, file_name):
    name = file["name"].replace(" ", "_")
    if name[-4:] == ".pdf":
        return save_pdf(file, f"{file_name}.pdf")
    return save_any_format_image_as(file["file"]["url"], file_name)

def save_pdf(file, name):
    image_location = os.path.join(STATIC_DIR, name)
    urllib.request.urlretrieve(file["file"]["url"], image_location)
    return name