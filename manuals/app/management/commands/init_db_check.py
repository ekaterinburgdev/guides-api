from app.internal.infrastructure.db_check import db_check_v2
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        db_check_v2.check_db()
