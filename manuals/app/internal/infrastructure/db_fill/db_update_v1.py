import os
import urllib.request

import environ
from app.models import PageElement
from django.conf import settings
from notion_client import Client

from .contents import SECTIONS

BASE_DIR = settings.BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
notion_client = Client(auth=env("INTEGRATION_TOKEN"))
STATIC_DIR = os.path.join(os.path.join(BASE_DIR, "app"), "static")


def check_db():
    check_sections()


def check_sections():
    for section in SECTIONS:
        check_section_content(section["id"])


def check_section_content(id):
    content = notion_client.blocks.children.list(id)
    column_ids = list(map(lambda x: x["id"], content["results"]))
    page_element = PageElement(id=id, content={"items": column_ids}, type="column_list")
    page_element.save()
    for column_id in column_ids:
        check_column_list_content(column_id)


def check_column_list_content(id):
    content = notion_client.blocks.children.list(id)
    element_ids = list(map(lambda x: x["id"], content["results"]))
    page_element = PageElement(id=id, content={"items": element_ids}, type="column_list")
    page_element.save()
    for element_id in element_ids:
        check_column_content(element_id)


def check_column_content(id):
    content = notion_client.blocks.children.list(id)

    item_ids = list(map(lambda x: x["id"], content["results"]))
    page_element = PageElement(id=id, content={"items": item_ids}, type="column")
    page_element.save()

    for item in content["results"]:
        if item["type"] == "paragraph":
            page_element = PageElement(
                id=item["id"],
                content={
                    "paragraph": [
                        {"text": item["paragraph"]["text"][0]["text"]},
                        {"annotations": item["paragraph"]["text"][0]["annotations"]},
                    ]
                },
                type="paragraph",
            )
            page_element.save()
        if item["type"] == "image":
            image_id = item["id"]
            image_name = f"{image_id}.png"
            image_location = os.path.join(STATIC_DIR, image_name)
            urllib.request.urlretrieve(item["image"]["file"]["url"], os.path.join(BASE_DIR, image_location))
            page_element = PageElement(id=image_id, content={"image": image_name}, type="image")
            page_element.save()
