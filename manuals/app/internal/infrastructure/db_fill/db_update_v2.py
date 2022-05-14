from app.internal.infrastructure.notion_client import NotionClient
from app.models import PageElement

from .content_getters import get_default_element_content, get_image_element_content_webp
from .contents import INFRASTRUCTURE_PAGES, SECTIONS

notion_client = NotionClient().notion_client


def check_db():
    for section in SECTIONS:
        check_page(section["id"])
    for page in INFRASTRUCTURE_PAGES:
        check_page(page["id"])


def check_page(id):
    page = notion_client.blocks.retrieve(id)
    check_page_element(page)


def check_page_element(page_element):
    print(page_element["id"])
    is_edited, edited_time = edited_check(page_element)

    if is_edited:
        update_element(page_element, edited_time)


def update_element(page_element, edited_time):
    element_id = page_element["id"]
    element_type = page_element["type"]
    if element_type == "image":
        element_content = get_image_element_content_webp(page_element)
    else:
        element_content = get_default_element_content(page_element, element_type)

    if not page_element["has_children"]:

        save_element(element_id, element_type, element_content, [], edited_time)
        return

    children = notion_client.blocks.children.list(element_id)
    children_ids = list(map(lambda x: x["id"], children["results"]))

    for child in children["results"]:
        check_page_element(child)

    save_element(element_id, element_type, element_content, children_ids, edited_time)


def save_element(element_id, element_type, element_content, element_children, edited_time):
    db_item = PageElement(
        id=element_id,
        type=element_type,
        content={"content": element_content},
        children={"children": element_children},
        last_edited=edited_time,
    )
    db_item.save()


def edited_check(item):
    id = item["id"]
    db_item = PageElement.objects.filter(id=id).first()
    if not db_item:
        if "last_edited_time" not in item.keys():
            return True, ""
        return True, item["last_edited_time"]

    last_edited_time = item["last_edited_time"]
    db_last_edited_time = db_item.last_edited
    return (last_edited_time != db_last_edited_time), item["last_edited_time"]
