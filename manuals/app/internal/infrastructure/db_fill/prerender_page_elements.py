from typing import List, Optional
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
        update_or_create_result = PrerenderedPageElement.objects.update_or_create(id=page.id, defaults={"content": content})
        try:
            if update_or_create_result[1]:
                text_content = prerender_text(content)
                data = update_or_create_result[0]
                data.text_content = text_content
                data.save()
        except Exception as e:
            print("Text render has been failed")
            print(e)
    for child in node.child_nodes.all():
        prerender_all(child)

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
