import os
import urllib.request

from .constants import BASE_DIR, STATIC_DIR


def get_image_element_content(item):
    image_id = item["id"]
    image_name = f"{image_id}.png"
    image_location = os.path.join(STATIC_DIR, image_name)
    urllib.request.urlretrieve(item["image"]["file"]["url"], image_location)
    return {"image_name": image_name, "image_data": item["image"]}


def get_default_element_content(item, type):
    if type in item.keys():
        return item[type]
    return "none"
