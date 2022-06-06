from app.models import PageElement

from .constants import ESCAPE_TYPES, FOLDER_TYPES


def serialize_page_element_by_id(page_element_id):
    page_element = PageElement.objects.filter(id=page_element_id).first()
    return serialize_page_element(page_element)


def serialize_page_element(page_element):
    if not page_element:
        print(f"ALARM!!!!!!!!! {page_element} element is missing!!!!")
        return None

    element_type = page_element.type
    element_content = page_element.content
    element_children = page_element.children.order_by("order").all()
    children_content = list(
        map(lambda x: serialize_page_element(x), filter(lambda x: x.type not in ESCAPE_TYPES, element_children))
    )
    children_content = pack_lists(children_content)

    serialized_element = {
        "id": page_element.id,
        "type": element_type,
        "content": element_content["content"],
        "children": children_content,
    }

    return serialized_element


# TODO: Stupid realization. Make better
def pack_lists(items):
    new_items = []
    current_list_item_type = None
    current_list_item_section = False
    current_list_item_list = []

    for item in items:
        if item["type"] not in FOLDER_TYPES.keys():
            if current_list_item_section:
                folder = {"type": FOLDER_TYPES[current_list_item_type], "children": current_list_item_list}
                new_items.append(folder)
                current_list_item_type = None
                current_list_item_section = False
                current_list_item_list = []
            new_items.append(item)
            continue
        if current_list_item_section:
            if item["type"] != current_list_item_type:
                folder = {"type": FOLDER_TYPES[current_list_item_type], "children": current_list_item_list}
                new_items.append(folder)
                current_list_item_type = item["type"]
                current_list_item_list = []
            current_list_item_list.append(item)
            continue
        current_list_item_type = item["type"]
        current_list_item_section = True
        current_list_item_list.append(item)

    return new_items
