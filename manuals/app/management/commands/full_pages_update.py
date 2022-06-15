from app.internal.infrastructure.db_fill import db_update_v4, page_tree_update
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        page_tree_update.update_page_tree()
        db_update_v4.check_db()
