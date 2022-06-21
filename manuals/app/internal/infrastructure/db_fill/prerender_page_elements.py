from app.models import PageTreeNode, PrerenderedPageElement
from app.internal.infrastructure.serialization.default_page_JSON_serialization import forced_serialize_page_element_by_id
from .contents import ROOT_PAGE_ID


def prerender_all(node=None):
    if not node:
        id = ROOT_PAGE_ID
        node = PageTreeNode.objects.filter(id=id).first()
    print(node.id)
    page = node.child_page
    if page:
        content = forced_serialize_page_element_by_id(page.id)
        PrerenderedPageElement.objects.update_or_create(id=page.id, defaults={"content": content})
    for child in node.child_nodes.all():
        prerender_all(child)
