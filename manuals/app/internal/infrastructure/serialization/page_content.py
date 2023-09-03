from app.models import PageTreeNode


def get_node_by_url(url: str):
    path_elements = url.split("/")
    if not path_elements:
        return None
    root_url = path_elements[0]
    if root_url == "root":
        path_elements = path_elements[1:]
    root_node = PageTreeNode.objects.filter(url="root").first()
    if not root_node:
        return None
    curr = root_node
    for next in path_elements:
        curr = get_url_node(next, curr)
        if not curr:
            return None
    return curr


def get_url_node(url, parent_object):
    node = parent_object.child_nodes.filter(url=url).first()
    if not node:
        return None
    if node not in parent_object.child_nodes.all():
        return None
    return node
