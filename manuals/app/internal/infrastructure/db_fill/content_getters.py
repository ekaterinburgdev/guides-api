import os
import urllib.request

from PIL import Image

from .constants import STATIC_DIR


def save_webp_cover(url, name):
    jpg_image_name = save_jpg_image(url, name)
    image_location = os.path.join(STATIC_DIR, jpg_image_name)
    return convert_jpg_to_webp(image_location, name)


def get_image_element_content_webp(item):
    image_id = item["id"]
    jpg_image_name = save_jpg_image(item["image"]["file"]["url"], image_id)
    image_location = os.path.join(STATIC_DIR, jpg_image_name)
    webp_image_name = convert_jpg_to_webp(image_location, image_id)
    return {"image_name": webp_image_name, "image_data": item["image"]}


def get_image_element_content_jpg(item):
    image_id = item["id"]
    jpg_image_name = save_jpg_image(item["image"]["file"]["url"], image_id)
    return {"image_name": jpg_image_name, "image_data": item["image"]}


def save_jpg_image(url, id):
    image_name = f"{id}.jpg"
    image_location = os.path.join(STATIC_DIR, image_name)
    urllib.request.urlretrieve(url, image_location)
    return image_name


def convert_jpg_to_webp(img_path, new_img_name):
    new_name = f"{new_img_name}.webp"
    new_image_location = os.path.join(STATIC_DIR, new_name)
    Image.open(img_path).convert("RGB").save(f"{new_image_location}", "webp")
    return new_name


def get_default_element_content(item, type):
    if type in item.keys():
        return item[type]
    return "none"
