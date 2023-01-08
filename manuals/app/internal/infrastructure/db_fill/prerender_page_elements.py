import copy
from typing import List, Optional
from app.models import PageTreeNode, PrerenderedPageElement
from app.internal.infrastructure.serialization.default_page_JSON_serialization import forced_serialize_page_element_by_id
from .contents import ROOT_PAGE_ID

UNKNOWN_SECTION_NAME = "Неизвестная секция"


def prerender_all():
    PrerenderedPageElement.objects.all().delete()
    id = ROOT_PAGE_ID
    node = PageTreeNode.objects.filter(id=id).first()
    section_name = get_section_name(node)
    print(node.id)
    page = node.child_page
    if page:
        content = forced_serialize_page_element_by_id(page.id)
        text_content = ""
        try:
            text_content = prerender_text(content)
        except Exception as e:
            print("Text render has been failed")
            print(e)
        PrerenderedPageElement.objects.update_or_create(id=page.id, defaults={
            "content": content,
            "url": "root",
            "text_content": text_content,
            "nodes_trace": {"ids": [id]},
            "section_name": section_name})
    for child in node.child_nodes.all():
        prerender_node(child, child.id, [id])

def prerender_node(node, guide_id: str, nodes_trace: List[str], prev_url: str=None):
    print(node.id)
    section_name = get_section_name(node)
    page = node.child_page
    url = node.url
    new_trace = copy.copy(nodes_trace)
    new_trace.append(node.id)
    if prev_url:
        url = f"{prev_url}/{url}"
    if page:
        content = forced_serialize_page_element_by_id(page.id)
        text_content = ""
        try:
            text_content = prerender_text(content)
        except Exception as e:
            print("Text render has been failed")
            print(e)
        PrerenderedPageElement.objects.update_or_create(id=page.id, defaults={
            "content": content,
            "guide_id": guide_id,
            "url": url,
            "text_content": text_content,
            "nodes_trace": {"ids": new_trace},
            "section_name": section_name})
    for child in node.child_nodes.all():
        prerender_node(child, guide_id, new_trace, prev_url=url)

def prerender_text(content_json: dict) -> str:
    texts = get_page_plain_text_contents(content_json)
    return " ".join(texts)

def get_page_plain_text_contents(content_json: dict) -> List[str]:
    text = extract_plain_text(content_json)
    if not text:
        text = []
    
    for child in content_json["children"]:
        child_text_contents = get_page_plain_text_contents(child)
        text.extend(child_text_contents)
    
    return text

def extract_plain_text(content_json: dict) -> Optional[List[str]]:
    content = content_json.get("content")
    if not content:
        return None
    texts = content.get("text")
    if not texts:
        return None
    result = []
    for text in texts:
        plain_text = text.get("plain_text")
        if not plain_text:
            continue
        if not isinstance(plain_text, str):
            print(f"Plain text is not str. Content: <<<{plain_text}>>>")
            continue
        result.append(plain_text)
    
    return result

def get_section_name(node: PageTreeNode):
    content = node.properties
    props = content.get("properties")
    if not props:
        return UNKNOWN_SECTION_NAME
    name = props.get("Name")
    if not name:
        return UNKNOWN_SECTION_NAME
    titles = name.get("title")
    if not titles:
        return UNKNOWN_SECTION_NAME
    if len(titles) < 1:
        return UNKNOWN_SECTION_NAME
    title = titles[0]
    title_plain_text = title.get("plain_text")
    if not title_plain_text:
        return UNKNOWN_SECTION_NAME
    return title_plain_text

