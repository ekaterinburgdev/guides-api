from app.internal.infrastructure.db_fill import db_update_v4, page_tree_update, prerender_page_elements
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        page_tree_update.update_page_tree()
        db_update_v4.check_db()
        prerender_page_elements.prerender_all()
