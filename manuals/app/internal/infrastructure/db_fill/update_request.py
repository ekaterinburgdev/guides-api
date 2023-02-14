from typing import List, Optional, Tuple
from app.models import PageTreeNode
from app.internal.infrastructure.serialization.page_content import get_node_by_url


class UpdateRequest:
    def __init__(self, page_tree_node: Optional[PageTreeNode] = None, force_update: bool = False) -> None:
        self.page_tree_node = page_tree_node
        self.force_update = force_update
    
def from_command(args: List[str]) -> Tuple[Optional[UpdateRequest], Optional[str]]:
    #TODO: options
    options = list(filter(lambda x: x.startswith("-"), args))
    force = "--force" in options or "-f" in options

    page_urls = list(filter(lambda x: not x.startswith("--"), args))
    if len(page_urls) == 0:
        return UpdateRequest(None, force), None
    
    if len(page_urls) > 1:
        return None, f"Я не понимаю, кого из них апдейтить: {', '.join(page_urls)}"
    
    page_url = page_urls[0]
    node = get_node_by_url(page_url)
    if not node:
        return None, f"У меня нет страницы по такому пути: {page_url}"
    
    return UpdateRequest(node, force), None
