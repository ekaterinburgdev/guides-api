import mimetypes
import os
import urllib.request
from urllib.parse import urlparse

from PIL import Image

from .constants import EXTENSIONS, STATIC_DIR


def save_webp_cover(url, name):
    jpg_image_name = save_jpg_image(url, name)
    image_location = os.path.join(STATIC_DIR, jpg_image_name)
    return convert_jpg_to_webp(image_location, name)


def get_image_element_content_webp(item):
    image_id = item["id"]
    print(item["image"]["file"]["url"])
    image_name = save_any_format_image(item["image"]["file"]["url"], image_id)
    if image_name[-4:] == ".jpg":
        image_location = os.path.join(STATIC_DIR, image_name)
        image_name = convert_jpg_to_webp(image_location, image_id)
    return {"image_name": image_name, "image_data": item["image"]}


def get_image_element_content_jpg(item):
    image_id = item["id"]
    jpg_image_name = save_jpg_image(item["image"]["file"]["url"], image_id)
    return {"image_name": jpg_image_name, "image_data": item["image"]}


def save_any_format_image(url, id):
    data_type = mimetypes.guess_type(urlparse(url).path)
    print(data_type)
    data_type = data_type[0]
    extension = ".jpg"
    if data_type in EXTENSIONS.keys():
        extension = EXTENSIONS[data_type]
    image_name = f"{id}{extension}"
    image_location = os.path.join(STATIC_DIR, image_name)
    urllib.request.urlretrieve(url, image_location)
    return image_name

def save_any_format_image_as(url, name):
    data_type = mimetypes.guess_type(urlparse(url).path)
    print(data_type)
    data_type = data_type[0]
    extension = ".jpg"
    if data_type in EXTENSIONS.keys():
        extension = EXTENSIONS[data_type]
    image_name = f"{name}{extension}"
    image_location = os.path.join(STATIC_DIR, image_name)
    urllib.request.urlretrieve(url, image_location)

    if image_name[-4:] != ".svg":
        image_name = convert_jpg_to_webp(image_location, name)
    
    return image_name

def save_jpg_image(url, id):
    image_name = f"{id}.jpg"
    image_location = os.path.join(STATIC_DIR, image_name)
    urllib.request.urlretrieve(url, image_location)
    return image_name


def convert_jpg_to_webp(img_path, new_img_name):
    new_name = f"{new_img_name}.webp"
    new_image_location = os.path.join(STATIC_DIR, new_name)
    Image.open(img_path).convert("RGBA").save(f"{new_image_location}", "webp")
    return new_name


def get_default_element_content(item, type):
    if type in item.keys():
        return item[type]
    return "none"
