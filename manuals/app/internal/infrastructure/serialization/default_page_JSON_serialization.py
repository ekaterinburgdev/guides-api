from app.models import PageElement


def serialize_page_element(page_element_id):
    page_element = PageElement.objects.filter(id=page_element_id)
    if len(page_element) == 0:
        return {"Missing content": "None"}

    page_element = page_element.first()
    element_type = page_element.type
    element_content = page_element.content
    element_children = page_element.children
    children_content = list(map(lambda x: {x: serialize_page_element(x)}, element_children["children"]))

    serialized_element = {
        "id": page_element_id,
        "type": element_type,
        "content": element_content["content"],
        "children": children_content,
    }

    return serialized_element
