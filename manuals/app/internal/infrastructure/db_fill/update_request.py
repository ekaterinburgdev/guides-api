from typing import List, Optional, Tuple
from app.models import PageTreeNode


class UpdateRequest:
    def __init__(self, page_tree_node: PageTreeNode = None, force_update: bool = False) -> None:
        self.page_tree_node = page_tree_node
        self.force_update = force_update
    
def from_command(args: List[str]) -> Tuple[Optional[UpdateRequest], Optional[str]]:
    #TODO: options
    options = list(filter(lambda x: x.startswith("--"), args))
    force = "--force" in options

    page_ids = list(filter(lambda x: not x.startswith("--"), args))
    if len(page_ids) == 0:
        return UpdateRequest(None, force), None
    
    if len(page_ids) > 1:
        return None, f"Я не понимаю, кого из них апдейтить: {', '.join(page_ids)}"
    
    page_id = page_ids[0]
    node = PageTreeNode.objects.filter(id=page_id).first()
    if not node:
        return None, f"У меня нет страницы с таким идентификатором: {page_id}"
    
    return UpdateRequest(node, force), None
