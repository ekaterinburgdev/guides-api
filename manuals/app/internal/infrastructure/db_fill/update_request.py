from app.models import PageTreeNode


class UpdateRequest:
    def __init__(self, page_tree_node: PageTreeNode = None, force_update: bool = False) -> None:
        self.page_tree_node = page_tree_node
        self.force_update = force_update