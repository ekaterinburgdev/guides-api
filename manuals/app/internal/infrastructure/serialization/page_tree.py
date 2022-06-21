from app.internal.infrastructure.db_fill.contents import ROOT_PAGE_ID
from app.models import PageTreeNode

ROOT_PAGE_CHILDREN_ORDER = {
    "d322a36b-21ab-4e40-9186-4205813263e2": 1,
    "52f4b5f5-5abc-4e76-b044-e836832e7bb7": 2,
    "c02e663a-61e3-44d6-a9a5-1503d87a40c2": 0,
    "cbd51ee4-565b-4620-b72e-f587a19279e5": 3,
    "other": 999999,
}


def tree_json(id):
    node = PageTreeNode.objects.filter(id=id).first()
    if not node:
        return None

    child_page_id = node.id
    properties = node.properties
    child_nodes = node.child_nodes.all()
    children = []
    for child_node in child_nodes:
        child = tree_json(child_node.id)
        children.append(child)

    children = list(
        filter(
            lambda x: (
                "properties" not in x
                or "Published" not in x["properties"]
                or "checkbox" not in x["properties"]["Published"]
            )
            or x["properties"]["Published"]["checkbox"],
            children,
        )
    )

    ordered_children = list(
        filter(
            lambda x: "properties" in x and "order" in x["properties"] and "number" in x["properties"]["order"],
            children,
        )
    )
    if len(ordered_children) == len(children):
        children = sorted(children, key=lambda x: x["properties"]["order"]["number"] if x["properties"]["order"]["number"] else 9999)
    else:
        children = sorted(
            children,
            key=lambda x: ROOT_PAGE_CHILDREN_ORDER[x["id"]]
            if x["id"] in ROOT_PAGE_CHILDREN_ORDER
            else ROOT_PAGE_CHILDREN_ORDER["other"],
        )

    return {
        "id": child_page_id,
        "cover": properties["cover"],
        "properties": properties["properties"],
        "children": children,
    }
