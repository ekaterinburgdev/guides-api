from app.internal.infrastructure.db_fill import db_update_v4
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("update_v4 start")
        db_update_v4.check_db(force_update=True)
