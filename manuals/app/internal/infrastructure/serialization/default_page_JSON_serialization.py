from app.models import PageElement

from .constants import FOLDER_TYPES


def serialize_page_element(page_element_id):
    page_element = PageElement.objects.filter(id=page_element_id)
    if len(page_element) == 0:
        print(f"ALARM!!!!!!!!! {page_element_id} element is missing!!!!")
        return {"Missing content": "None"}

    page_element = page_element.first()
    element_type = page_element.type
    element_content = page_element.content
    element_children = page_element.children
    children_content = list(map(lambda x: serialize_page_element(x), element_children["children"]))
    children_content = pack_lists(children_content)

    serialized_element = {
        "id": page_element_id,
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
