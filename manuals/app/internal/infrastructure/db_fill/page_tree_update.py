from datetime import datetime

from app.internal.infrastructure.notion_client import NotionClient
from app.models import PageTreeNode
from .file_save import save_file

from .content_getters import save_webp_cover
from .contents import ROOT_PAGE_ID

notion_client = NotionClient()


def update_page_tree():
    root_page_info = notion_client.page(ROOT_PAGE_ID)
    root_page_children = build_child_databases_tree(ROOT_PAGE_ID)
    root_page_last_edited_time = datetime.fromisoformat(root_page_info["last_edited_time"][:-1] + "+00:00")
    db_child_child_page = None
    existedNode = PageTreeNode.objects.filter(id=ROOT_PAGE_ID).first()
    if existedNode:
        db_child_child_page = existedNode.child_page
    root_node = PageTreeNode(
        id=ROOT_PAGE_ID,
        child_page=db_child_child_page,
        properties={"cover": None, "properties": root_page_info},
        last_edited=root_page_last_edited_time,
        url="root",
    )
    root_node.save()
    children_ids = [x.id for x in root_page_children]
    children_to_exclude = root_node.child_nodes.exclude(id__in=children_ids).all()
    root_node.child_nodes.remove(*children_to_exclude)
    root_node.child_nodes.add(*root_page_children)


def build_child_databases_tree(id):
    """Search databases on page. Recursively calls itself for every founded databases element (page). Returns element's database children nodes list"""
    page_dbs = list(filter(lambda x: x["type"] == "child_database", notion_client.page_children(id)["results"]))
    children = []
    for db in page_dbs:
        db_children = notion_client.db_children(db["id"])["results"]
        for db_child in db_children:
            db_child_id = db_child["id"]
            print(db_child_id)
            db_child_properties = db_child["properties"]
            db_child_url = db_child_properties["pageUrl"]["url"]
            db_child_cover = None
            if db_child["cover"]:
                cover_type = db_child["cover"]["type"]
                cover_url = db_child["cover"][cover_type]["url"]
                db_child_cover = save_webp_cover(cover_url, db_child_id)
            db_child_last_edited_time = datetime.fromisoformat(db_child["last_edited_time"][:-1] + "+00:00")
            db_child_children = build_child_databases_tree(db_child_id)
            db_child_child_page = None
            existedNode = PageTreeNode.objects.filter(id=db_child_id).first()
            if existedNode:
                db_child_child_page = existedNode.child_page
            new_props = convert_properties(db_child_properties, db_child_id)
            db_child_page_node = PageTreeNode(
                id=db_child_id,
                child_page=db_child_child_page,
                properties={"cover": db_child_cover, "properties": new_props},
                last_edited=db_child_last_edited_time,
                url=db_child_url,
            )
            db_child_page_node.save()
            children_ids = [x.id for x in db_child_children]
            children_to_exclude = db_child_page_node.child_nodes.exclude(id__in=children_ids).all()
            db_child_page_node.child_nodes.remove(*children_to_exclude)
            db_child_page_node.child_nodes.add(*db_child_children)
            children.append(db_child_page_node)
    return children

def convert_properties(properties: dict, id: str):
    new_props = dict()
    for prop in properties.keys():
        value = properties[prop]
        if value["type"] == "files":
            files = []
            for i in range(len(value["files"])):
                file = value["files"][i]
                name = save_file(file, f"{id}_{prop}_{i}")
                files.append(name)
            new_props[prop] = files
        else:
            new_props["prop"] = value
    return new_props