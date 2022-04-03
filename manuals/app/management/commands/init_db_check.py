from django.core.management.base import BaseCommand
from app.internal.infrastructure.db_check import db_check


class Command(BaseCommand):
    def handle(self, *args, **options):
        db_check.check_db()
