from app.models import PageTreeNode


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

    return {
        "id": child_page_id,
        "cover": properties["cover"],
        "properties": properties["properties"],
        "children": children,
    }
