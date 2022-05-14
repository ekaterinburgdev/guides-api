from app.internal.infrastructure.db_fill import db_update_v3
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        db_update_v3.check_db()
