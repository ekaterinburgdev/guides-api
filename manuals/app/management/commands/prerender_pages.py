from app.internal.infrastructure.db_fill import prerender_page_elements
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        prerender_page_elements.prerender_all()
